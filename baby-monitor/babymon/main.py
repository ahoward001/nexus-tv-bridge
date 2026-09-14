"""BabyMon entry point.

  babymon run       start monitoring (this is what the LaunchAgent runs)
  babymon test      send a test alert on every enabled channel
  babymon devices   list microphones and cameras by name
  babymon doctor    check config, model, permissions and Tailscale
"""

from __future__ import annotations

import argparse
import logging
import logging.handlers
import signal
import subprocess
import sys
import time

from . import config as cfgmod
from .alerts import Notifier
from .escalate import Escalator
from .motion import Camera
from .stream import StreamServer, tailscale_ipv4

log = logging.getLogger("babymon")


def _setup_logging(verbose: bool = False) -> None:
    cfgmod.LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s")
    root = logging.getLogger()
    root.setLevel(logging.DEBUG if verbose else logging.INFO)

    stderr = logging.StreamHandler(sys.stderr)
    stderr.setFormatter(fmt)
    root.addHandler(stderr)

    rotating = logging.handlers.RotatingFileHandler(
        cfgmod.LOG_PATH, maxBytes=2_000_000, backupCount=3
    )
    rotating.setFormatter(fmt)
    root.addHandler(rotating)


class _Caffeine:
    """Hold macOS awake while monitoring. A sleeping laptop hears nothing."""

    def __init__(self) -> None:
        self._proc = None

    def __enter__(self):
        try:
            self._proc = subprocess.Popen(
                ["caffeinate", "-dimsu"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            log.info("holding the Mac awake (caffeinate)")
        except FileNotFoundError:
            log.warning("caffeinate not found -- make sure this Mac won't sleep")
        return self

    def __exit__(self, *exc):
        if self._proc is not None:
            self._proc.terminate()


def cmd_run(args) -> int:
    cfg = cfgmod.load()
    notifier = Notifier(cfg.alerts)
    escalator = Escalator(cfg.alerts, notifier)

    camera = None
    if cfg.motion.enabled or cfg.stream.enabled:
        camera = Camera(cfg.motion, width=cfg.stream.width)
        camera.start()

    server = StreamServer(cfg.stream, camera, escalator)
    server.start()

    # Imported late so `babymon doctor` still works without an audio stack.
    from .detector import CryDetector

    detector = CryDetector(cfg.detect, str(cfgmod.MODEL_PATH))
    detector.start()

    stopping = {"now": False}

    def _bye(signum, frame):
        stopping["now"] = True

    signal.signal(signal.SIGTERM, _bye)
    signal.signal(signal.SIGINT, _bye)

    log.info("BabyMon is watching. Ctrl-C to stop.")
    with _Caffeine():
        try:
            while not stopping["now"]:
                escalator.tick()

                crying, conf, label = detector.crying()
                if crying:
                    escalator.trigger("cry", conf, label, cfg.detect.cooldown_seconds)
                elif camera is not None and camera.available:
                    moving, ratio = camera.moving()
                    if moving:
                        escalator.trigger(
                            "motion", ratio, "movement", cfg.motion.cooldown_seconds
                        )

                time.sleep(0.5)
        finally:
            log.info("shutting down")
            detector.stop()
            if camera is not None:
                camera.stop()
            server.stop()
    return 0


def cmd_test(args) -> int:
    cfg = cfgmod.load()
    results = Notifier(cfg.alerts).self_test()
    if not results:
        print("No alert channels are enabled.")
        return 1
    failed = 0
    for r in results:
        if r.ok:
            print(f"  ok      {r.channel}")
        else:
            failed += 1
            print(f"  FAILED  {r.channel}: {r.detail}")
    if failed:
        print("\nFix the failures above before relying on this monitor.")
    else:
        print("\nAll channels delivered. Check your phone to confirm you got them.")
    return 1 if failed else 0


def cmd_devices(args) -> int:
    try:
        import sounddevice as sd
    except Exception as exc:
        print(f"Could not load the audio library: {exc}")
        return 1

    print("Microphones (use the name in detect.input_device):")
    for i, d in enumerate(sd.query_devices()):
        if d["max_input_channels"] > 0:
            print(f"  [{i}] {d['name']}")

    print("\nCameras (use the index in motion.camera_index):")
    try:
        import cv2

        found = False
        for idx in range(4):
            cap = cv2.VideoCapture(idx)
            if cap.isOpened():
                print(f"  [{idx}] available")
                found = True
            cap.release()
        if not found:
            print("  none found (or macOS has not granted camera access yet)")
    except Exception as exc:
        print(f"  could not probe cameras: {exc}")
    return 0


def cmd_doctor(args) -> int:
    problems = 0

    def check(label, ok, detail=""):
        nonlocal problems
        print(f"  {'ok     ' if ok else 'PROBLEM'} {label}" + (f" -- {detail}" if detail else ""))
        if not ok:
            problems += 1

    print("Config")
    try:
        cfg = cfgmod.load()
        check(f"{cfgmod.CONFIG_PATH}", True)
    except Exception as exc:
        check(f"{cfgmod.CONFIG_PATH}", False, str(exc))
        return 1

    print("\nCry model")
    exists = cfgmod.MODEL_PATH.exists()
    check(
        f"{cfgmod.MODEL_PATH.name}",
        exists,
        "" if exists else "missing -- run scripts/fetch_model.py",
    )
    try:
        import mediapipe  # noqa: F401
        check("mediapipe (YAMNet classifier)", True)
    except Exception as exc:
        check("mediapipe (YAMNet classifier)", False, f"{exc} -- will use energy fallback")

    print("\nHardware")
    try:
        import sounddevice as sd
        ins = [d for d in sd.query_devices() if d["max_input_channels"] > 0]
        check("microphone", bool(ins), f"{len(ins)} input device(s)")
    except Exception as exc:
        check("microphone", False, str(exc))

    if cfg.motion.enabled or cfg.stream.enabled:
        try:
            import cv2
            cap = cv2.VideoCapture(cfg.motion.camera_index)
            ok = cap.isOpened()
            cap.release()
            check("camera", ok, "" if ok else "check System Settings > Privacy > Camera")
        except Exception as exc:
            check("camera", False, str(exc))

    print("\nLive view")
    if cfg.stream.enabled and cfg.stream.bind == "tailscale":
        ip = tailscale_ipv4()
        check("tailscale", ip is not None, ip or "not running -- phone viewing unavailable")
        if ip:
            print(f"         open http://{ip}:{cfg.stream.port}/ on your phone")
    else:
        print("         disabled or localhost-only")

    print("\nAlerts")
    for name, ch in (
        ("ntfy", cfg.alerts.ntfy),
        ("pushover", cfg.alerts.pushover),
        ("twilio", cfg.alerts.twilio),
    ):
        print(f"  {'enabled ' if ch.enabled else 'off     '} {name}")
    print("\n  run `babymon test` to actually send one.")

    print(f"\n{problems} problem(s) found.")
    return 1 if problems else 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="babymon", description="Local-only baby monitor.")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("run", help="start monitoring").set_defaults(fn=cmd_run)
    sub.add_parser("test", help="send a test alert everywhere").set_defaults(fn=cmd_test)
    sub.add_parser("devices", help="list mics and cameras").set_defaults(fn=cmd_devices)
    sub.add_parser("doctor", help="check the setup").set_defaults(fn=cmd_doctor)

    args = p.parse_args(argv)
    _setup_logging(args.verbose)
    try:
        return args.fn(args)
    except cfgmod.ConfigError as exc:
        print(f"\nConfig problem:\n  {exc}\n", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
