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
    pushes: int = 0        # how many times we've re-pushed
    calls: int = 0         # how many times we've dialled


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

        sent = self.notifier.push_all(title, body, expire=self._expire_for(inc))
        inc.pushes = 1
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

    def _expire_for(self, inc: Incident) -> int | None:
        """How long Pushover should keep re-alerting on its own."""
        p = self.cfg.persist
        if not p.enabled:
            return None
        if not p.max_minutes:
            return 10800          # API maximum; our loop nags past it via ntfy
        return int(p.max_minutes * 60)

    def _alert_text(self, inc: Incident) -> tuple[str, str]:
        """Repeat alerts say how long this has been going on."""
        mins = max(1, int((time.time() - inc.started) / 60))
        noun = "crying" if inc.kind == "cry" else "movement"
        return (
            f"STILL {noun.upper()}",
            f"Unacknowledged for {mins} minute{'s' if mins != 1 else ''}. "
            f"Tap to acknowledge and silence.",
        )

    def _watch(self, inc: Incident) -> None:
        """Nag until acknowledged, or until we give up.

        Three independent clocks run here:
          * ntfy re-push, every persist.repeat_seconds
          * the phone call, first at escalate_after_seconds then every
            persist.recall_seconds
          * the overall give-up deadline, persist.max_minutes

        Pushover is deliberately NOT re-sent: its server already re-alerts
        every retry_seconds until acknowledged, so re-sending would stack
        sirens instead of repeating one.
        """
        p = self.cfg.persist
        now = time.time()
        give_up = (inc.started + p.max_minutes * 60) if (p.enabled and p.max_minutes) else None
        next_push = (inc.started + p.repeat_seconds) if p.enabled else None
        next_call = inc.started + self.cfg.escalate_after_seconds
        can_call = self._will_call(inc.kind)

        if not can_call and not p.enabled:
            # Nothing further would ever happen; don't spin.
            return self._resolve(inc, "no escalation configured for this alert type")

        while True:
            if inc.acknowledged_at:
                return self._resolve(inc, "acknowledged")
            if self._poll_receipts(inc):
                return self._resolve(inc, "acknowledged on Pushover")

            now = time.time()
            if give_up is not None and now >= give_up:
                log.error(
                    "gave up after %d alerts and %d calls over %.0f minutes with no "
                    "acknowledgement -- CHECK ON THE BABY",
                    inc.pushes, inc.calls, p.max_minutes,
                )
                return self._resolve(inc, "gave up unacknowledged")

            # -- repeat push ------------------------------------------------
            if next_push is not None and now >= next_push:
                title, body = self._alert_text(inc)
                # ntfy only; Pushover is still re-alerting from the first send.
                self.notifier.push_all(title, body, pushover=False)
                inc.pushes += 1
                next_push = now + p.repeat_seconds
                log.warning("re-alert #%d (unacknowledged)", inc.pushes)

            # -- phone call -------------------------------------------------
            if can_call and now >= next_call:
                say = (
                    "Baby monitor alert. Crying detected in the nursery."
                    if inc.kind == "cry"
                    else "Baby monitor alert. Movement detected in the crib."
                )
                result = self.notifier.call(say)
                inc.called = True
                inc.calls += 1
                with self._lock:
                    self.state = State.ESCALATED
                log.warning(
                    "call #%d: %s", inc.calls,
                    "placed" if result.ok else f"FAILED {result.detail}",
                )
                if not p.enabled:
                    return self._resolve(inc, "call placed" if result.ok else "call failed")
                next_call = now + p.recall_seconds

            if not p.enabled and not can_call:
                return self._resolve(inc, "nothing left to escalate")

            # Sleep until the next scheduled event, but never past it.
            upcoming = [t for t in (next_push, next_call if can_call else None, give_up)
                        if t is not None and t > now]
            wait = min(upcoming) - now if upcoming else _POLL_SECONDS
            time.sleep(min(_POLL_SECONDS, max(0.02, wait)))

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
