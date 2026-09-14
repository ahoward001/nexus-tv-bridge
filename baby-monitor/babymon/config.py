"""Config loading and validation."""

from __future__ import annotations

import os
import stat
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import tomllib  # py3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

CONFIG_DIR = Path(os.path.expanduser("~/.config/babymon"))
CONFIG_PATH = CONFIG_DIR / "config.toml"
STATE_DIR = Path(os.path.expanduser("~/Library/Application Support/BabyMon"))
MODEL_PATH = STATE_DIR / "models" / "yamnet.tflite"
LOG_PATH = STATE_DIR / "babymon.log"


class ConfigError(RuntimeError):
    pass


@dataclass
class DetectCfg:
    backend: str = "auto"
    cry_threshold: float = 0.45
    sustain_seconds: float = 4.0
    cooldown_seconds: float = 180.0
    input_device: str = ""
    watch_classes: list[str] = field(
        default_factory=lambda: [
            "Baby cry, infant cry",
            "Crying, sobbing",
            "Whimper",
            "Screaming",
        ]
    )


@dataclass
class MotionCfg:
    enabled: bool = True
    camera_index: int = 0
    sensitivity: float = 0.035
    sustain_seconds: float = 8.0
    cooldown_seconds: float = 300.0


@dataclass
class NtfyCfg:
    enabled: bool = False
    server: str = "https://ntfy.sh"
    topic: str = ""
    priority: int = 5


@dataclass
class PushoverCfg:
    enabled: bool = False
    user_key: str = ""
    api_token: str = ""
    retry_seconds: int = 30
    expire_seconds: int = 600
    sound: str = "siren"


@dataclass
class TwilioCfg:
    enabled: bool = False
    account_sid: str = ""
    auth_token: str = ""
    from_number: str = ""
    to_number: str = ""
    say: str = "Baby monitor alert. Crying detected in the nursery."


@dataclass
class PersistCfg:
    """Keep re-alerting until you actually acknowledge."""
    enabled: bool = True
    repeat_seconds: float = 120.0    # re-push this often
    recall_seconds: float = 300.0    # re-call this often
    max_minutes: float = 60.0        # give up after this long (0 = never)


@dataclass
class AlertsCfg:
    escalate_after_seconds: float = 60.0
    escalate_motion_alerts: bool = False
    persist: PersistCfg = field(default_factory=PersistCfg)
    ntfy: NtfyCfg = field(default_factory=NtfyCfg)
    pushover: PushoverCfg = field(default_factory=PushoverCfg)
    twilio: TwilioCfg = field(default_factory=TwilioCfg)


@dataclass
class StreamCfg:
    enabled: bool = True
    bind: str = "tailscale"
    port: int = 8477
    username: str = "parent"
    password: str = ""
    fps: int = 6
    width: int = 640


@dataclass
class Config:
    detect: DetectCfg = field(default_factory=DetectCfg)
    motion: MotionCfg = field(default_factory=MotionCfg)
    alerts: AlertsCfg = field(default_factory=AlertsCfg)
    stream: StreamCfg = field(default_factory=StreamCfg)


def _fill(cls, raw: dict[str, Any]):
    """Build a dataclass from a dict, ignoring unknown keys."""
    known = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
    return cls(**{k: v for k, v in raw.items() if k in known})


def load(path: Path | None = None) -> Config:
    path = path or CONFIG_PATH
    if not path.exists():
        raise ConfigError(
            f"No config at {path}.\n"
            f"Run the installer, or copy config.example.toml there and edit it."
        )

    _warn_if_world_readable(path)

    with path.open("rb") as fh:
        raw = tomllib.load(fh)

    alerts_raw = raw.get("alerts", {})
    alerts = _fill(AlertsCfg, alerts_raw)
    alerts.ntfy = _fill(NtfyCfg, alerts_raw.get("ntfy", {}))
    alerts.pushover = _fill(PushoverCfg, alerts_raw.get("pushover", {}))
    alerts.twilio = _fill(TwilioCfg, alerts_raw.get("twilio", {}))
    alerts.persist = _fill(PersistCfg, alerts_raw.get("persist", {}))

    cfg = Config(
        detect=_fill(DetectCfg, raw.get("detect", {})),
        motion=_fill(MotionCfg, raw.get("motion", {})),
        alerts=alerts,
        stream=_fill(StreamCfg, raw.get("stream", {})),
    )
    validate(cfg)
    return cfg


def _warn_if_world_readable(path: Path) -> None:
    mode = path.stat().st_mode
    if mode & (stat.S_IRGRP | stat.S_IROTH):
        print(
            f"[babymon] WARNING: {path} is readable by other accounts on this Mac "
            f"and contains your API keys. Fix with:  chmod 600 {path}",
            file=sys.stderr,
        )


def validate(cfg: Config) -> None:
    a = cfg.alerts
    enabled = [
        name
        for name, ch in (("ntfy", a.ntfy), ("pushover", a.pushover), ("twilio", a.twilio))
        if ch.enabled
    ]
    if not enabled:
        raise ConfigError(
            "No alert channel is enabled. A monitor that cannot reach you is "
            "worse than none at all -- enable at least one of [alerts.ntfy], "
            "[alerts.pushover] or [alerts.twilio]."
        )

    if a.ntfy.enabled and not a.ntfy.topic:
        raise ConfigError("[alerts.ntfy] is enabled but 'topic' is empty.")
    if a.ntfy.enabled and len(a.ntfy.topic) < 16:
        print(
            "[babymon] WARNING: your ntfy topic is short and therefore guessable. "
            "Anyone who guesses it can read your alerts. Use 24+ random characters.",
            file=sys.stderr,
        )

    if a.pushover.enabled and not (a.pushover.user_key and a.pushover.api_token):
        raise ConfigError("[alerts.pushover] is enabled but user_key/api_token are empty.")

    if a.twilio.enabled:
        t = a.twilio
        missing = [
            k for k in ("account_sid", "auth_token", "from_number", "to_number")
            if not getattr(t, k)
        ]
        if missing:
            raise ConfigError(f"[alerts.twilio] is enabled but missing: {', '.join(missing)}")
        for k in ("from_number", "to_number"):
            if not getattr(t, k).startswith("+"):
                raise ConfigError(
                    f"[alerts.twilio] {k} must be E.164 format starting with '+', "
                    f"e.g. +15551234567"
                )

    if a.twilio.enabled and not (a.ntfy.enabled or a.pushover.enabled):
        if a.escalate_after_seconds > 0:
            print(
                "[babymon] NOTE: Twilio is your only channel, so there is no push to "
                "acknowledge. Calling immediately instead of waiting "
                f"{a.escalate_after_seconds:.0f}s.",
                file=sys.stderr,
            )
            a.escalate_after_seconds = 0.0

    if cfg.stream.enabled:
        if cfg.stream.bind not in ("tailscale", "localhost"):
            raise ConfigError(
                "[stream] bind must be 'tailscale' or 'localhost'. Binding the video "
                "stream to a public or LAN-wide address is exactly how baby cams get "
                "hijacked, so it is deliberately not an option here."
            )
        if not cfg.stream.password or len(cfg.stream.password) < 12:
            raise ConfigError(
                "[stream] password must be at least 12 characters. Set a strong one "
                "or disable the stream."
            )

    p = a.persist
    if p.enabled:
        if p.repeat_seconds < 30:
            raise ConfigError(
                "[alerts.persist] repeat_seconds below 30 is a notification storm. "
                "You will mute the app, which defeats the point. Use 60 or more."
            )
        if p.recall_seconds < 60:
            raise ConfigError(
                "[alerts.persist] recall_seconds below 60 would dial you faster than "
                "a call can complete. Use 120 or more."
            )
        if p.max_minutes and p.max_minutes * 60 < p.repeat_seconds:
            raise ConfigError(
                "[alerts.persist] max_minutes is shorter than repeat_seconds, so you "
                "would only ever get one alert."
            )
        if p.max_minutes == 0:
            print(
                "[babymon] NOTE: persist.max_minutes is 0 -- alerts will repeat "
                "forever until acknowledged.",
                file=sys.stderr,
            )

    if not 0.0 < cfg.detect.cry_threshold < 1.0:
        raise ConfigError("[detect] cry_threshold must be between 0 and 1.")
    if cfg.detect.sustain_seconds < 1.0:
        raise ConfigError(
            "[detect] sustain_seconds below 1.0 will fire on doors and traffic. "
            "Use 2.0 or higher."
        )
