"""Integration test for the live-view server.

Proves the things that actually matter for privacy: an unauthenticated
request gets nothing, a wrong password gets nothing, and the server refuses
to bind anywhere reachable from outside your own devices.
"""

import base64, json, sys, unittest, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from babymon.config import Config, ConfigError, validate
from babymon.escalate import Escalator
from babymon.stream import StreamServer


class FakeNotifier:
    def push_all(self, t, m): return []
    def call(self, say=None): return None
    def pushover_acknowledged(self, r): return False
    def pushover_cancel(self, r): pass


class FakeCamera:
    available = False           # no OpenCV needed for these assertions
    def latest_frame(self): return None


def _get(url, user=None, pw=None, method="GET"):
    req = urllib.request.Request(url, method=method)
    if user is not None:
        tok = base64.b64encode(f"{user}:{pw}".encode()).decode()
        req.add_header("Authorization", f"Basic {tok}")
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


class TestStreamAuth(unittest.TestCase):
    PW = "correct-horse-battery"

    @classmethod
    def setUpClass(cls):
        cfg = Config().stream
        cfg.enabled = True
        cfg.bind = "localhost"
        cfg.port = 8899
        cfg.username = "parent"
        cfg.password = cls.PW
        cls.esc = Escalator(Config().alerts, FakeNotifier())
        cls.srv = StreamServer(cfg, FakeCamera(), cls.esc)
        cls.srv.start()
        cls.base = "http://127.0.0.1:8899"

    @classmethod
    def tearDownClass(cls):
        cls.srv.stop()

    def test_no_credentials_is_rejected(self):
        for path in ("/", "/status", "/stream.mjpg"):
            code, body = _get(self.base + path)
            self.assertEqual(code, 401, f"{path} leaked without auth")
            self.assertNotIn(b"Nursery", body)

    def test_wrong_password_is_rejected(self):
        code, _ = _get(self.base + "/", "parent", "hunter2")
        self.assertEqual(code, 401)

    def test_wrong_username_is_rejected(self):
        code, _ = _get(self.base + "/", "admin", self.PW)
        self.assertEqual(code, 401)

    def test_correct_credentials_get_the_page(self):
        code, body = _get(self.base + "/", "parent", self.PW)
        self.assertEqual(code, 200)
        self.assertIn(b"Nursery", body)

    def test_status_reports_state(self):
        code, body = _get(self.base + "/status", "parent", self.PW)
        self.assertEqual(code, 200)
        st = json.loads(body)
        self.assertEqual(st["state"], "idle")
        self.assertIn("cooldown_remaining", st)

    def test_ack_requires_auth(self):
        code, _ = _get(self.base + "/ack", method="POST")
        self.assertEqual(code, 401)

    def test_unknown_path_is_404_not_a_traversal(self):
        code, _ = _get(self.base + "/../../etc/passwd", "parent", self.PW)
        self.assertIn(code, (400, 404))

    def test_stream_without_camera_is_503_not_a_crash(self):
        code, _ = _get(self.base + "/stream.mjpg", "parent", self.PW)
        self.assertEqual(code, 503)

    def test_bound_only_to_loopback(self):
        """The socket must not be listening on a LAN-reachable address."""
        host = self.srv._httpd.server_address[0]
        self.assertEqual(host, "127.0.0.1")
        self.assertNotIn(host, ("0.0.0.0", "::"))


class TestStreamConfigRefusesPublicBind(unittest.TestCase):
    def test_wide_open_bind_is_a_config_error(self):
        for bad in ("0.0.0.0", "lan", "::", "public"):
            c = Config()
            c.alerts.ntfy.enabled = True
            c.alerts.ntfy.topic = "t" * 24
            c.stream.password = "a-long-enough-password"
            c.stream.bind = bad
            with self.assertRaises(ConfigError, msg=f"{bad} was accepted"):
                validate(c)


if __name__ == "__main__":
    unittest.main(verbosity=2)
