"""Outbound alert channels.

Only text leaves this machine here -- a short title and message. No audio,
no frames, no model output beyond a confidence number.
"""

from __future__ import annotations

import logging
import xml.sax.saxutils as sax
from dataclasses import dataclass

import requests

log = logging.getLogger("babymon.alerts")

_TIMEOUT = 12


@dataclass
class Sent:
    channel: str
    ok: bool
    detail: str = ""
    receipt: str = ""     # Pushover emergency receipt, used for ack polling


class Notifier:
    def __init__(self, cfg):
        self.cfg = cfg

    # -- ntfy --------------------------------------------------------------

    def ntfy(self, title: str, message: str, priority: int | None = None) -> Sent:
        c = self.cfg.ntfy
        url = f"{c.server.rstrip('/')}/{c.topic}"
        try:
            r = requests.post(
                url,
                data=message.encode("utf-8"),
                headers={
                    "Title": title,
                    "Priority": str(priority if priority is not None else c.priority),
                    "Tags": "rotating_light,baby",
                },
                timeout=_TIMEOUT,
            )
            r.raise_for_status()
            return Sent("ntfy", True)
        except Exception as exc:
            log.error("ntfy failed: %s", exc)
            return Sent("ntfy", False, str(exc))

    # -- Pushover ----------------------------------------------------------

    def pushover(
        self, title: str, message: str, emergency: bool = True,
        expire: int | None = None,
    ) -> Sent:
        c = self.cfg.pushover
        payload = {
            "token": c.api_token,
            "user": c.user_key,
            "title": title,
            "message": message,
            "priority": 2 if emergency else 1,
            "sound": c.sound,
        }
        if emergency:
            # Emergency priority re-alerts until acknowledged. That acknowledgement
            # is also what cancels the phone call, so we keep the receipt.
            payload["retry"] = max(30, int(c.retry_seconds))
            # 10800s (3h) is the Pushover API maximum.
            payload["expire"] = min(10800, int(expire or c.expire_seconds))
        try:
            r = requests.post(
                "https://api.pushover.net/1/messages.json", data=payload, timeout=_TIMEOUT
            )
            body = r.json() if r.content else {}
            if r.status_code != 200 or body.get("status") != 1:
                errs = "; ".join(body.get("errors", [])) or f"HTTP {r.status_code}"
                log.error("pushover rejected the message: %s", errs)
                return Sent("pushover", False, errs)
            return Sent("pushover", True, receipt=body.get("receipt", ""))
        except Exception as exc:
            log.error("pushover failed: %s", exc)
            return Sent("pushover", False, str(exc))

    def pushover_acknowledged(self, receipt: str) -> bool:
        if not receipt:
            return False
        try:
            r = requests.get(
                f"https://api.pushover.net/1/receipts/{receipt}.json",
                params={"token": self.cfg.pushover.api_token},
                timeout=_TIMEOUT,
            )
            return bool(r.json().get("acknowledged"))
        except Exception as exc:
            log.debug("receipt poll failed: %s", exc)
            return False

    def pushover_cancel(self, receipt: str) -> None:
        """Stop an emergency alert re-alerting, e.g. once you've acked in the web UI."""
        if not receipt:
            return
        try:
            requests.post(
                f"https://api.pushover.net/1/receipts/{receipt}/cancel.json",
                data={"token": self.cfg.pushover.api_token},
                timeout=_TIMEOUT,
            )
        except Exception as exc:
            log.debug("receipt cancel failed: %s", exc)

    # -- Twilio ------------------------------------------------------------

    def call(self, say: str | None = None) -> Sent:
        c = self.cfg.twilio
        spoken = sax.escape(say or c.say)
        twiml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            "<Response>"
            f'<Say voice="alice">{spoken}</Say>'
            '<Pause length="1"/>'
            f'<Say voice="alice">{spoken}</Say>'
            "</Response>"
        )
        try:
            r = requests.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{c.account_sid}/Calls.json",
                auth=(c.account_sid, c.auth_token),
                data={"To": c.to_number, "From": c.from_number, "Twiml": twiml},
                timeout=_TIMEOUT,
            )
            if r.status_code >= 300:
                detail = ""
                try:
                    detail = r.json().get("message", "")
                except Exception:
                    detail = r.text[:200]
                log.error("twilio call failed (HTTP %s): %s", r.status_code, detail)
                return Sent("twilio", False, detail or f"HTTP {r.status_code}")
            log.info("placed call to %s", c.to_number)
            return Sent("twilio", True)
        except Exception as exc:
            log.error("twilio failed: %s", exc)
            return Sent("twilio", False, str(exc))

    # -- helpers -----------------------------------------------------------

    def push_all(
        self,
        title: str,
        message: str,
        *,
        ntfy: bool = True,
        pushover: bool = True,
        expire: int | None = None,
    ) -> list[Sent]:
        """Fire the enabled push channels. Returns what happened on each.

        The channel flags exist because Pushover re-alerts on its own server
        until you acknowledge it, while ntfy does not. When we are nagging on
        a loop we re-send ntfy each round but leave Pushover alone, otherwise
        every round would stack another independent siren on your phone.
        """
        out: list[Sent] = []
        if ntfy and self.cfg.ntfy.enabled:
            out.append(self.ntfy(title, message))
        if pushover and self.cfg.pushover.enabled:
            out.append(self.pushover(title, message, emergency=True, expire=expire))
        return out

    def self_test(self) -> list[Sent]:
        """Send a harmless test on every enabled channel. Used by the installer."""
        title = "BabyMon test"
        msg = "Setup test. If you can see this, alerts are working."
        out = list(self.push_all(title, msg))
        if self.cfg.twilio.enabled:
            out.append(self.call("This is a test call from your baby monitor. Setup is working."))
        return out
