"""Incident state machine: push first, phone call if you don't answer.

    detected -> push (ntfy + Pushover emergency)
             -> wait `escalate_after_seconds` for an acknowledgement
             -> no ack? place the phone call
             -> ack (phone, or the Acknowledge button on the live view page)
                cancels the Pushover re-alerts and starts the cooldown
"""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, field
from enum import Enum

log = logging.getLogger("babymon.escalate")

# How often to ask Pushover whether you've acknowledged, while we wait.
_POLL_SECONDS = 2.0


class State(str, Enum):
    IDLE = "idle"
    ALERTING = "alerting"      # push out, waiting for you
    ESCALATED = "escalated"    # phone call placed
    COOLDOWN = "cooldown"      # handled; staying quiet


@dataclass
class Incident:
    kind: str                  # "cry" or "motion"
    started: float
    confidence: float
    label: str
    cooldown: float = 180.0
    receipts: list[str] = field(default_factory=list)
    called: bool = False
    acknowledged_at: float | None = None


class Escalator:
    def __init__(self, cfg_alerts, notifier):
        self.cfg = cfg_alerts
        self.notifier = notifier
        self.state = State.IDLE
        self.incident: Incident | None = None
        self.last_incident: Incident | None = None
        self._cooldown_until = 0.0
        self._lock = threading.RLock()

    # -- queries -----------------------------------------------------------

    def suppressed(self) -> bool:
        return time.time() < self._cooldown_until

    def status(self) -> dict:
        with self._lock:
            inc = self.incident or self.last_incident
            return {
                "state": self.state.value,
                "kind": inc.kind if inc else None,
                "confidence": round(inc.confidence, 3) if inc else None,
                "label": inc.label if inc else None,
                "started": inc.started if inc else None,
                "called": inc.called if inc else False,
                "acknowledged": bool(inc and inc.acknowledged_at),
                "cooldown_remaining": max(0, round(self._cooldown_until - time.time())),
            }

    # -- lifecycle ---------------------------------------------------------

    def trigger(self, kind: str, confidence: float, label: str, cooldown: float) -> None:
        with self._lock:
            if self.state is not State.IDLE or self.suppressed():
                return
            inc = Incident(
                kind=kind,
                started=time.time(),
                confidence=confidence,
                label=label,
                cooldown=cooldown,
            )
            self.incident = inc
            self.state = State.ALERTING

        when = time.strftime("%-I:%M %p", time.localtime(inc.started))
        if kind == "cry":
            title = "Baby crying"
            body = f"{label.capitalize()} detected at {when} ({confidence:.0%} confidence)."
        else:
            title = "Movement in the crib"
            body = f"Sustained movement detected at {when}."

        sent = self.notifier.push_all(title, body)
        for s in sent:
            if s.ok and s.receipt:
                inc.receipts.append(s.receipt)
        ok = [s.channel for s in sent if s.ok]
        bad = [f"{s.channel}({s.detail[:60]})" for s in sent if not s.ok]
        log.warning("ALERT %s: %s | pushed=%s failed=%s", kind, body, ok or "none", bad or "none")

        if not ok and not self._will_call(kind):
            log.error(
                "every push channel failed and escalation is off for %s alerts -- "
                "you were NOT notified", kind,
            )

        threading.Thread(target=self._watch, args=(inc,), name="escalate", daemon=True).start()

    def _will_call(self, kind: str) -> bool:
        if not self.cfg.twilio.enabled:
            return False
        if kind == "motion" and not self.cfg.escalate_motion_alerts:
            return False
        return True

    def _watch(self, inc: Incident) -> None:
        """Wait out the grace period, then call if nobody acknowledged."""
        deadline = inc.started + self.cfg.escalate_after_seconds
        while time.time() < deadline:
            if inc.acknowledged_at:
                return self._resolve(inc, "acknowledged before escalation")
            if self._poll_receipts(inc):
                return self._resolve(inc, "acknowledged on Pushover")
            time.sleep(min(_POLL_SECONDS, max(0.02, deadline - time.time())))

        if not self._will_call(inc.kind):
            return self._resolve(inc, "no escalation configured for this alert type")

        with self._lock:
            if inc.acknowledged_at:
                return self._resolve(inc, "acknowledged at the deadline")
            self.state = State.ESCALATED

        say = (
            "Baby monitor alert. Crying detected in the nursery."
            if inc.kind == "cry"
            else "Baby monitor alert. Movement detected in the crib."
        )
        result = self.notifier.call(say)
        inc.called = True
        log.warning("escalated to phone call: %s", "placed" if result.ok else f"FAILED {result.detail}")
        self._resolve(inc, "call placed" if result.ok else "call failed")

    def _poll_receipts(self, inc: Incident) -> bool:
        if not self.cfg.pushover.enabled:
            return False
        for rcpt in inc.receipts:
            if self.notifier.pushover_acknowledged(rcpt):
                inc.acknowledged_at = time.time()
                return True
        return False

    def acknowledge(self) -> bool:
        """Called from the live-view page's Acknowledge button."""
        with self._lock:
            inc = self.incident
            if inc is None:
                return False
            inc.acknowledged_at = time.time()
        for rcpt in inc.receipts:
            self.notifier.pushover_cancel(rcpt)
        log.info("acknowledged locally")
        return True

    def _resolve(self, inc: Incident, why: str) -> None:
        with self._lock:
            if self.incident is not inc:
                return
            self.last_incident = inc
            self.incident = None
            self.state = State.COOLDOWN
            self._cooldown_until = time.time() + inc.cooldown
        log.info("incident resolved (%s); quiet for %ds", why, int(inc.cooldown))

    def tick(self) -> None:
        with self._lock:
            if self.state is State.COOLDOWN and not self.suppressed():
                self.state = State.IDLE
