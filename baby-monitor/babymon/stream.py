"""Private live view.

Security model, in order of importance:

 1. The socket binds to your Tailscale address only. A tailnet address is not
    routable from the public internet and not reachable from other devices on
    your local wifi -- only from devices signed into your own Tailscale
    account. There is no port to forward and nothing for a scanner to find.
 2. Tailscale carries it over WireGuard, so the traffic is encrypted
    device-to-device even though this server speaks plain HTTP.
 3. HTTP Basic auth on top, compared in constant time, so a device that joins
    your tailnet still can't open the feed without the password.
 4. Frames are read from RAM and encoded per-request. Nothing is recorded and
    no video ever reaches a third-party server or an AI model.

If Tailscale isn't running, the server binds to 127.0.0.1 and says so rather
than silently falling back to a wide-open address.
"""

from __future__ import annotations

import base64
import json
import logging
import secrets
import shutil
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

log = logging.getLogger("babymon.stream")

_TS_BINARIES = (
    "tailscale",
    "/usr/local/bin/tailscale",
    "/opt/homebrew/bin/tailscale",
    "/Applications/Tailscale.app/Contents/MacOS/Tailscale",
)

_PAGE = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nursery</title>
<style>
  :root{color-scheme:dark}
  body{margin:0;background:#0b0d10;color:#e8eaed;
       font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
  header{padding:14px 16px;display:flex;align-items:center;gap:10px;
         border-bottom:1px solid #22262c}
  .dot{width:10px;height:10px;border-radius:50%;background:#3fb950;flex:none}
  .dot.alert{background:#f85149;animation:p 1s infinite}
  @keyframes p{50%{opacity:.25}}
  h1{font-size:15px;font-weight:600;margin:0}
  #meta{margin-left:auto;font-size:13px;color:#9099a5}
  img{display:block;width:100%;max-width:100%;background:#000}
  .wrap{padding:16px;max-width:820px;margin:0 auto}
  button{width:100%;padding:14px;font-size:16px;font-weight:600;border:0;
         border-radius:10px;background:#f85149;color:#fff;margin-top:14px}
  button[disabled]{background:#22262c;color:#6e7681}
  .note{font-size:12px;color:#6e7681;margin-top:14px}
</style>
<header>
  <span class="dot" id="dot"></span>
  <h1>Nursery</h1>
  <span id="meta">connecting…</span>
</header>
<div class="wrap">
  <img src="/stream.mjpg" alt="Live view of the nursery">
  <button id="ack" disabled>Acknowledge alert</button>
  <p class="note">Private to your tailnet. Nothing here is recorded or uploaded.</p>
</div>
<script>
const dot=document.getElementById('dot'),meta=document.getElementById('meta'),
      ack=document.getElementById('ack');
async function poll(){
  try{
    const s=await (await fetch('/status',{cache:'no-store'})).json();
    const live=s.state==='alerting'||s.state==='escalated';
    dot.className='dot'+(live?' alert':'');
    ack.disabled=!live;
    meta.textContent=live
      ? (s.kind==='cry'?'Crying':'Movement')+' · '+Math.round((s.confidence||0)*100)+'%'
      : (s.cooldown_remaining>0?'Quiet for '+s.cooldown_remaining+'s':'All quiet');
  }catch(e){meta.textContent='offline';}
}
ack.onclick=async()=>{ack.disabled=true;await fetch('/ack',{method:'POST'});poll();};
poll();setInterval(poll,2000);
</script>
"""


def tailscale_ipv4() -> str | None:
    for cand in _TS_BINARIES:
        exe = shutil.which(cand) or (cand if cand.startswith("/") else None)
        if not exe:
            continue
        try:
            out = subprocess.run(
                [exe, "ip", "-4"], capture_output=True, text=True, timeout=6
            )
        except Exception:
            continue
        addr = out.stdout.strip().splitlines()
        if out.returncode == 0 and addr and addr[0].startswith("100."):
            return addr[0].strip()
    return None


def _handler_factory(cfg, camera, escalator):
    token = base64.b64encode(
        f"{cfg.username}:{cfg.password}".encode("utf-8")
    ).decode("ascii")
    frame_interval = 1.0 / max(1, cfg.fps)

    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        server_version = "BabyMon"
        sys_version = ""

        def log_message(self, fmt, *args):
            log.debug("%s - %s", self.address_string(), fmt % args)

        # -- auth ----------------------------------------------------------

        def _authed(self) -> bool:
            hdr = self.headers.get("Authorization", "")
            if not hdr.startswith("Basic "):
                return False
            return secrets.compare_digest(hdr[6:].strip(), token)

        def _challenge(self) -> None:
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Nursery"')
            self.send_header("Content-Length", "0")
            self.end_headers()

        def _guard(self) -> bool:
            if self._authed():
                return True
            # Slow down anyone grinding the password.
            time.sleep(0.75)
            self._challenge()
            return False

        # -- responses -----------------------------------------------------

        def _send(self, code, body: bytes, ctype="text/html; charset=utf-8"):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            if not self._guard():
                return
            if self.path.rstrip("/") == "/ack":
                ok = escalator.acknowledge()
                self._send(200, json.dumps({"acknowledged": ok}).encode(), "application/json")
            else:
                self._send(404, b"not found", "text/plain")

        def do_GET(self):
            if not self._guard():
                return
            path = self.path.split("?", 1)[0].rstrip("/") or "/"
            if path == "/":
                self._send(200, _PAGE.encode("utf-8"))
            elif path == "/status":
                st = escalator.status()
                st["camera"] = camera.available if camera else False
                self._send(200, json.dumps(st).encode(), "application/json")
            elif path == "/stream.mjpg":
                self._stream()
            else:
                self._send(404, b"not found", "text/plain")

        def _stream(self):
            if camera is None or not camera.available:
                self._send(503, b"camera unavailable", "text/plain")
                return
            try:
                import cv2
            except Exception:
                # No OpenCV means no live view, but alerting is untouched.
                self._send(503, b"video support not installed", "text/plain")
                return
            self.send_response(200)
            self.send_header(
                "Content-Type", "multipart/x-mixed-replace; boundary=frame"
            )
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            try:
                while True:
                    frame = camera.latest_frame()
                    if frame is not None:
                        ok, buf = cv2.imencode(
                            ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70]
                        )
                        if ok:
                            jpg = buf.tobytes()
                            self.wfile.write(b"--frame\r\n")
                            self.wfile.write(b"Content-Type: image/jpeg\r\n")
                            self.wfile.write(
                                f"Content-Length: {len(jpg)}\r\n\r\n".encode()
                            )
                            self.wfile.write(jpg)
                            self.wfile.write(b"\r\n")
                    time.sleep(frame_interval)
            except (BrokenPipeError, ConnectionResetError):
                pass  # viewer closed the tab

    return Handler


class StreamServer:
    def __init__(self, cfg, camera, escalator):
        self.cfg = cfg
        self.camera = camera
        self.escalator = escalator
        self._httpd = None
        self.url = ""

    def start(self) -> None:
        if not self.cfg.enabled:
            log.info("live view disabled in config")
            return

        if self.cfg.bind == "tailscale":
            host = tailscale_ipv4()
            if host is None:
                host = "127.0.0.1"
                log.warning(
                    "Tailscale is not running, so the live view is bound to this "
                    "laptop only (127.0.0.1) and your phone cannot reach it. "
                    "Start Tailscale and restart BabyMon to enable phone viewing. "
                    "Refusing to bind a wider address."
                )
        else:
            host = "127.0.0.1"

        handler = _handler_factory(self.cfg, self.camera, self.escalator)
        self._httpd = ThreadingHTTPServer((host, self.cfg.port), handler)
        self._httpd.daemon_threads = True
        self.url = f"http://{host}:{self.cfg.port}/"
        threading.Thread(
            target=self._httpd.serve_forever, name="stream", daemon=True
        ).start()
        log.info("live view on %s (password protected)", self.url)

    def stop(self) -> None:
        if self._httpd is not None:
            self._httpd.shutdown()
            self._httpd.server_close()
