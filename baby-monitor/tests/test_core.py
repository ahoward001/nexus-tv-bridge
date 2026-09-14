"""Offline tests: config validation, detection logic, escalation ladder.

No microphone, camera, or network required -- everything external is faked,
so this runs anywhere (including CI).
"""

import sys, time, types, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from babymon import config as cfgmod
from babymon.config import Config, ConfigError, validate
from babymon.detector import EnergyBackend, SAMPLE_RATE, _WINDOW
from babymon.escalate import Escalator, State

import numpy as np


def base_cfg() -> Config:
    c = Config()
    c.alerts.ntfy.enabled = True
    c.alerts.ntfy.topic = "babymon-" + "x" * 20
    c.stream.password = "a-long-enough-password"
    return c


class TestConfigValidation(unittest.TestCase):
    def test_accepts_a_sane_config(self):
        validate(base_cfg())

    def test_rejects_no_alert_channels(self):
        c = base_cfg()
        c.alerts.ntfy.enabled = False
        with self.assertRaisesRegex(ConfigError, "No alert channel"):
            validate(c)

    def test_rejects_public_stream_bind(self):
        c = base_cfg()
        c.stream.bind = "0.0.0.0"
        with self.assertRaisesRegex(ConfigError, "tailscale"):
            validate(c)

    def test_rejects_weak_stream_password(self):
        c = base_cfg()
        c.stream.password = "baby"
        with self.assertRaisesRegex(ConfigError, "12 characters"):
            validate(c)

    def test_rejects_non_e164_twilio_numbers(self):
        c = base_cfg()
        c.alerts.twilio.enabled = True
        c.alerts.twilio.account_sid = "AC1"
        c.alerts.twilio.auth_token = "tok"
        c.alerts.twilio.from_number = "5551234567"
        c.alerts.twilio.to_number = "+15559876543"
        with self.assertRaisesRegex(ConfigError, "E.164"):
            validate(c)

    def test_rejects_trigger_happy_sustain(self):
        c = base_cfg()
        c.detect.sustain_seconds = 0.5
        with self.assertRaisesRegex(ConfigError, "doors and traffic"):
            validate(c)

    def test_twilio_only_calls_immediately(self):
        c = base_cfg()
        c.alerts.ntfy.enabled = False
        c.alerts.twilio.enabled = True
        c.alerts.twilio.account_sid = "AC1"
        c.alerts.twilio.auth_token = "tok"
        c.alerts.twilio.from_number = "+15551234567"
        c.alerts.twilio.to_number = "+15559876543"
        validate(c)
        # No push exists to acknowledge, so waiting 60s would be dead time.
        self.assertEqual(c.alerts.escalate_after_seconds, 0.0)


class TestEnergyBackend(unittest.TestCase):
    """The no-ML fallback should stay quiet on a quiet room and react to a cry."""

    def setUp(self):
        self.be = EnergyBackend()
        self.t = np.arange(_WINDOW) / SAMPLE_RATE

    def _settle_noise_floor(self):
        rng = np.random.default_rng(0)
        for _ in range(60):
            self.be.score(rng.normal(0, 0.002, _WINDOW).astype(np.float32))

    def test_quiet_room_scores_zero(self):
        self._settle_noise_floor()
        rng = np.random.default_rng(1)
        quiet = rng.normal(0, 0.002, _WINDOW).astype(np.float32)
        self.assertLess(self.be.score(quiet).value, 0.1)

    def test_loud_cry_like_tone_scores_high(self):
        self._settle_noise_floor()
        # A cry: strong 500 Hz fundamental with harmonics, well above the floor.
        cry = sum(
            (0.35 / k) * np.sin(2 * np.pi * 500 * k * self.t) for k in (1, 2, 3, 4)
        ).astype(np.float32)
        self.assertGreater(self.be.score(cry).value, 0.4)

    def test_low_rumble_is_not_a_cry(self):
        """A truck outside is loud but its energy sits below the cry band."""
        self._settle_noise_floor()
        rumble = (0.6 * np.sin(2 * np.pi * 60 * self.t)).astype(np.float32)
        self.assertLess(self.be.score(rumble).value, 0.25)


class FakeNotifier:
    """Stands in for the real network calls."""

    def __init__(self, ack_after=None):
        self.pushes, self.calls, self.cancels, self.expires = [], [], [], []
        self._ack_after = ack_after
        self._first_poll = None

    def push_all(self, title, message, *, ntfy=True, pushover=True, expire=None):
        self.pushes.append((title, message))
        self.expires.append(expire)
        out = []
        if ntfy:
            out.append(types.SimpleNamespace(channel="ntfy", ok=True, receipt="", detail=""))
        if pushover:
            out.append(types.SimpleNamespace(channel="pushover", ok=True, receipt="r1", detail=""))
        return out

    def call(self, say=None):
        self.calls.append(say)
        return types.SimpleNamespace(channel="twilio", ok=True, receipt="", detail="")

    def pushover_acknowledged(self, receipt):
        if self._ack_after is None:
            return False
        self._first_poll = self._first_poll or time.time()
        return time.time() - self._first_poll >= self._ack_after

    def pushover_cancel(self, receipt):
        self.cancels.append(receipt)


class _EscalatorMixin:
    def _esc(self, notifier, escalate_after=0.4, twilio=True, motion_escalates=False,
             persist=False, repeat=0.3, recall=0.4, max_minutes=0.0):
        c = base_cfg()
        c.alerts.escalate_after_seconds = escalate_after
        c.alerts.escalate_motion_alerts = motion_escalates
        c.alerts.twilio.enabled = twilio
        c.alerts.persist.enabled = persist
        c.alerts.persist.repeat_seconds = repeat
        c.alerts.persist.recall_seconds = recall
        c.alerts.persist.max_minutes = max_minutes
        return Escalator(c.alerts, notifier)


class TestEscalation(_EscalatorMixin, unittest.TestCase):
    def test_push_then_call_when_ignored(self):
        n = FakeNotifier()
        e = self._esc(n)
        e.trigger("cry", 0.91, "Baby cry, infant cry", cooldown=5)
        self.assertEqual(len(n.pushes), 1)
        self.assertIn("91%", n.pushes[0][1])
        time.sleep(1.2)
        self.assertEqual(len(n.calls), 1, "should have escalated to a phone call")
        self.assertEqual(e.state, State.COOLDOWN)

    def test_local_ack_prevents_the_call(self):
        n = FakeNotifier()
        e = self._esc(n, escalate_after=1.5)
        e.trigger("cry", 0.8, "Baby cry, infant cry", cooldown=5)
        time.sleep(0.2)
        self.assertTrue(e.acknowledge())
        time.sleep(1.8)
        self.assertEqual(n.calls, [], "acknowledging must cancel the escalation")

    def test_pushover_ack_prevents_the_call(self):
        n = FakeNotifier(ack_after=0.1)
        e = self._esc(n, escalate_after=2.0)
        e.trigger("cry", 0.8, "Baby cry, infant cry", cooldown=5)
        time.sleep(1.0)
        self.assertEqual(n.calls, [])

    def test_cooldown_suppresses_a_second_alert(self):
        n = FakeNotifier()
        e = self._esc(n, escalate_after=0.1)
        e.trigger("cry", 0.9, "Baby cry, infant cry", cooldown=30)
        time.sleep(0.6)
        e.trigger("cry", 0.9, "Baby cry, infant cry", cooldown=30)
        self.assertEqual(len(n.pushes), 1, "cooldown should swallow the repeat")

    def test_motion_does_not_phone_you_by_default(self):
        n = FakeNotifier()
        e = self._esc(n, escalate_after=0.3, motion_escalates=False)
        e.trigger("motion", 0.05, "movement", cooldown=5)
        time.sleep(1.0)
        self.assertEqual(len(n.pushes), 1)
        self.assertEqual(n.calls, [], "motion is informational, not call-worthy")

    def test_motion_escalates_when_asked(self):
        n = FakeNotifier()
        e = self._esc(n, escalate_after=0.3, motion_escalates=True)
        e.trigger("motion", 0.05, "movement", cooldown=5)
        time.sleep(1.0)
        self.assertEqual(len(n.calls), 1)

    def test_concurrent_triggers_make_one_incident(self):
        n = FakeNotifier()
        e = self._esc(n, escalate_after=5)
        for _ in range(5):
            e.trigger("cry", 0.9, "Baby cry, infant cry", cooldown=30)
        self.assertEqual(len(n.pushes), 1)


class TestPersistence(_EscalatorMixin, unittest.TestCase):
    """The loop must keep nagging until acknowledged, then stop immediately."""

    def test_push_repeats_until_acknowledged(self):
        n = FakeNotifier()
        e = self._esc(n, escalate_after=99, twilio=False, persist=True, repeat=0.3)
        e.trigger("cry", 0.9, "Baby cry, infant cry", cooldown=5)
        time.sleep(1.4)
        self.assertGreaterEqual(len(n.pushes), 4, "should have re-pushed several times")
        e.acknowledge()
        time.sleep(0.4)
        settled = len(n.pushes)
        time.sleep(0.8)
        self.assertEqual(len(n.pushes), settled, "acknowledging must stop the nagging")

    def test_repeat_pushes_skip_pushover(self):
        """Pushover re-alerts server-side; re-sending would stack sirens."""
        n = FakeNotifier()
        e = self._esc(n, escalate_after=99, twilio=False, persist=True, repeat=0.3)
        e.trigger("cry", 0.9, "Baby cry, infant cry", cooldown=5)
        time.sleep(1.0)
        e.acknowledge()
        # Only the first push carries a Pushover send (receipt r1).
        self.assertEqual(n.pushes[0][0], "Baby crying")
        self.assertGreater(len(n.pushes), 1)

    def test_repeat_text_reports_elapsed_time(self):
        n = FakeNotifier()
        e = self._esc(n, escalate_after=99, twilio=False, persist=True, repeat=0.3)
        e.trigger("cry", 0.9, "Baby cry, infant cry", cooldown=5)
        time.sleep(0.8)
        e.acknowledge()
        self.assertIn("STILL CRYING", n.pushes[1][0])
        self.assertIn("Unacknowledged", n.pushes[1][1])

    def test_calls_repeat_on_their_own_interval(self):
        n = FakeNotifier()
        e = self._esc(n, escalate_after=0.1, persist=True, repeat=5.0, recall=0.4)
        e.trigger("cry", 0.9, "Baby cry, infant cry", cooldown=5)
        time.sleep(1.5)
        e.acknowledge()
        self.assertGreaterEqual(len(n.calls), 3, "should have re-dialled")

    def test_acknowledging_cancels_the_pushover_siren(self):
        n = FakeNotifier()
        e = self._esc(n, escalate_after=99, twilio=False, persist=True, repeat=0.3)
        e.trigger("cry", 0.9, "Baby cry, infant cry", cooldown=5)
        time.sleep(0.4)
        e.acknowledge()
        self.assertIn("r1", n.cancels, "must cancel the emergency receipt")

    def test_gives_up_after_max_minutes(self):
        n = FakeNotifier()
        e = self._esc(n, escalate_after=99, twilio=False, persist=True,
                      repeat=0.3, max_minutes=1.0 / 60)   # 1 second
        e.trigger("cry", 0.9, "Baby cry, infant cry", cooldown=5)
        time.sleep(1.6)
        self.assertEqual(e.state, State.COOLDOWN, "should stop rather than nag forever")
        settled = len(n.pushes)
        time.sleep(0.6)
        self.assertEqual(len(n.pushes), settled)

    def test_expire_covers_the_whole_nag_window(self):
        """Pushover must keep re-alerting for as long as we intend to nag."""
        n = FakeNotifier()
        e = self._esc(n, escalate_after=99, twilio=False, persist=True,
                      repeat=0.3, max_minutes=30)
        e.trigger("cry", 0.9, "Baby cry, infant cry", cooldown=5)
        time.sleep(0.2)
        e.acknowledge()
        self.assertEqual(n.expires[0], 1800)

    def test_expire_caps_at_the_api_maximum(self):
        n = FakeNotifier()
        e = self._esc(n, escalate_after=99, twilio=False, persist=True,
                      repeat=0.3, max_minutes=0)   # forever
        e.trigger("cry", 0.9, "Baby cry, infant cry", cooldown=5)
        time.sleep(0.2)
        e.acknowledge()
        self.assertEqual(n.expires[0], 10800)


class TestPersistValidation(unittest.TestCase):
    def test_rejects_storm_intervals(self):
        c = base_cfg()
        c.alerts.persist.repeat_seconds = 5
        with self.assertRaisesRegex(ConfigError, "notification storm"):
            validate(c)

    def test_rejects_recall_faster_than_a_call(self):
        c = base_cfg()
        c.alerts.persist.recall_seconds = 10
        with self.assertRaisesRegex(ConfigError, "faster than"):
            validate(c)

    def test_rejects_window_shorter_than_one_repeat(self):
        c = base_cfg()
        c.alerts.persist.repeat_seconds = 300
        c.alerts.persist.max_minutes = 2
        with self.assertRaisesRegex(ConfigError, "only ever get one alert"):
            validate(c)

    def test_defaults_are_valid(self):
        validate(base_cfg())


class TestTwiml(unittest.TestCase):
    def test_spoken_text_is_xml_escaped(self):
        """A stray & or < in the spoken line must not break the call payload."""
        from babymon.alerts import Notifier
        c = base_cfg()
        c.alerts.twilio.say = 'Baby & "friend" <crying>'
        captured = {}

        class FakeResp:
            status_code = 201
            def json(self): return {}

        import babymon.alerts as A
        orig = A.requests.post
        A.requests.post = lambda url, **kw: (captured.update(kw), FakeResp())[1]
        try:
            Notifier(c.alerts).call()
        finally:
            A.requests.post = orig

        twiml = captured["data"]["Twiml"]
        self.assertIn("&amp;", twiml)
        self.assertIn("&lt;crying&gt;", twiml)
        self.assertNotIn("<crying>", twiml)


if __name__ == "__main__":
    unittest.main(verbosity=2)
