# BabyMon

Turns a MacBook into a baby monitor. It listens for crying, optionally watches
for movement, and escalates to your phone until you acknowledge it.

**Nothing is recorded. Nothing is uploaded. No AI service sees or hears your
nursery.** The cry classifier is a 4 MB model file that runs on your own CPU.

---

## What it actually does

```
  mic ──► YAMNet cry classifier ──┐
                                  ├──► sustained? ──► ntfy + Pushover siren
  cam ──► motion detection ───────┘                        │
                                                           ├─ every 2 min: re-push
                                                           ├─ after 60s: phone rings
                                                           └─ every 5 min: rings again
                                                                    │
                                                        until you acknowledge
```

**It does not alert once and give up.** The siren repeats, the pushes repeat,
and the phone keeps ringing until you acknowledge — from the Pushover
notification or the **Acknowledge** button on the live-view page. One tap
silences all of it.

## Install

1. Download this folder to the MacBook.
2. Double-click **`install.command`**.
3. Answer the prompts. Click **Allow** when macOS asks for microphone and
   camera access.

The installer sets up everything in your user folder, downloads the model,
generates your secrets, sends a real test alert, and registers a login item.
It never asks for an admin password and never installs anything system-wide.

To start it right now: double-click **`start-monitor.command`**.
To remove it: double-click **`uninstall.command`**.

## Alert channels

| Channel | What you get | Cost |
|---|---|---|
| **ntfy** | Max-priority push with an alarm tone | Free, no account |
| **Pushover** | Siren that repeats every 30s until acknowledged | $5 once per platform |
| **Twilio** | Your phone actually rings | ~$1.15/mo + ~$0.02/call |

Enable as many as you like; blank entries are simply skipped.

### Overriding silent mode and Focus (do both of these)

Two independent ways to make a silenced phone make noise. Set up both — they
fail in different ways.

**1. Pushover Critical Alerts.** Pushover holds Apple's critical-alert
entitlement, which lets it ignore the hardware mute switch *and* Focus modes,
and play at its own volume rather than yours. It is **off by default** and no
API parameter turns it on — it is a receiver-side toggle you flip once:

> Pushover app → **Settings** → **Notification Settings** → enable
> **Critical Alerts** for emergency priority → approve the iOS dialog.

Without that toggle a silenced phone stays silent, no matter what BabyMon
sends. Since Pushover 4.2 the setting is split between high and emergency
priority; BabyMon sends emergency, so make sure that one is on.

**2. Twilio call with Emergency Bypass.**

1. Save your Twilio number as a contact (e.g. "Nursery").
2. Contact → **Edit** → **Ringtone** → turn on **Emergency Bypass**.

That contact now rings at full volume regardless of the mute switch or Focus.

Belt and braces: Critical Alerts can be revoked by a stray tap in iOS
Settings, and a call can be missed if cell service drops while wifi is fine.
Running both means one covering the other.

> ntfy has no critical-alert entitlement, so its push will *not* override a
> muted phone. It is the free fast layer, not the guarantee.

### Persistence

Configured under `[alerts.persist]`:

| Setting | Default | What it does |
|---|---|---|
| `repeat_seconds` | 120 | Re-push every 2 minutes |
| `recall_seconds` | 300 | Dial again every 5 minutes |
| `max_minutes` | 60 | Give up after an hour (`0` = never) |

Repeat alerts change their wording to **"STILL CRYING — unacknowledged for 6
minutes"**, so a glance tells you whether this is new or ongoing.

Pushover is deliberately **not** re-sent on that interval. Its server already
re-alerts every 30 seconds until you acknowledge, so re-sending would stack
independent sirens rather than repeat one. The repeat interval drives ntfy,
which has no retry of its own. Pushover's `expire` is sized automatically to
cover your whole nag window, capped at their 3-hour API maximum.

If `max_minutes` elapses with no acknowledgement, BabyMon stops and writes a
loud line to the log. It cannot do anything more useful than that — which is
the point at which somebody needs to physically check on the baby.

## Privacy and security

This is the part worth reading twice.

**Audio and video never leave the laptop.** Frames and audio live in a short
rolling buffer in RAM that is continuously overwritten. There is no recording
path in this codebase — no file writes, no uploads, no cloud storage bucket.
What goes out is a line of text: *"Baby cry detected at 2:14am, 91%."*

**No AI service is involved at runtime.** YAMNet is a TensorFlow Lite file on
your disk. There is no API call, no inference endpoint, nothing routed to
Anthropic or anyone else. The only network traffic is the alert itself.

**The live view has no public surface.** When `bind = "tailscale"` the server
binds only to your tailnet address (`100.x.y.z`). That address:

- is not routable from the public internet — there is nothing to port-scan;
- is not reachable from other devices on your wifi, or your neighbour's;
- is only reachable from devices signed into *your* Tailscale account;
- carries WireGuard encryption device-to-device.

On top of that the server requires a password, compared in constant time, and
rate-limits failures. If Tailscale isn't running it falls back to `127.0.0.1`
and logs a warning — it will **never** silently bind a wider address. The
config validator rejects `0.0.0.0` outright.

**Your secrets.** API keys live in `~/.config/babymon/config.toml`, `chmod 600`.
BabyMon warns on startup if that file becomes readable by other accounts.

**Your ntfy topic is a password.** Anyone who knows the topic name can read
your alerts. The installer generates a 24-character random one. Don't shorten it.

### Setting up Tailscale

Install the Tailscale app on the MacBook and on your phone, sign both into the
same account, done. No router config, no port forwarding, no static IP.
Run `babymon doctor` and it prints the exact URL to open on your phone.

## Day-to-day

```
babymon run       # start monitoring
babymon test      # send a test alert on every channel
babymon doctor    # check config, model, mic, camera, Tailscale
babymon devices   # list microphones and cameras by name
```

The shim lives at `~/Library/Application Support/BabyMon/bin/babymon`.
Logs are at `~/Library/Application Support/BabyMon/babymon.log`.

## Tuning

Everything is in `~/.config/babymon/config.toml`.

**Too many false alarms** — raise `cry_threshold` toward 0.6, or raise
`sustain_seconds` to 6. The default demands 4 seconds of sustained crying,
which already rejects doors, traffic and single squeaks.

**Missing real cries** — lower `cry_threshold` to 0.35 and confirm the right
microphone is selected with `babymon devices`. A laptop across a large room
with a fan running is a genuinely hard case; move it closer to the crib.

**Motion is too twitchy** — raise `motion.sensitivity`. Changing daylight
through a window will trip it; `0.06` is calmer for a bright nursery.

**Being phoned too eagerly** — raise `escalate_after_seconds`, or set
`escalate_motion_alerts = false` (the default) so only crying can call you.

**Too much nagging** — raise `repeat_seconds` and `recall_seconds`, or set
`persist.enabled = false` for a single alert with one follow-up call. The
validator refuses intervals under 30s (push) and 60s (call), because an alert
you mute out of irritation protects nobody.

## Known limitations — read these

- **This is not a medical device.** It is a convenience monitor. Do not rely
  on it to detect breathing problems, choking, or anything safety-critical,
  and don't let it replace checking on your child. It has no role in
  preventing SIDS.
- **Keep the laptop and its cord well away from the crib.** Cords are a
  strangulation hazard and laptops get hot. Put it on a dresser across the room.
- **A closed lid or a sleeping Mac hears nothing.** BabyMon runs `caffeinate`
  to hold the machine awake, but closing the lid still sleeps it unless the
  Mac is on power with an external display. Leave it open and plugged in.
- **Alerts need working internet on both ends.** If your wifi drops, no alert
  reaches your phone. Nothing on this laptop can fix that.
- **macOS permissions with the login item.** macOS sometimes refuses mic and
  camera access to a background service even after you approved it in Terminal.
  If `babymon doctor` shows no microphone, start it with
  `start-monitor.command` instead and leave that window open.
- **Cry detection is good, not perfect.** YAMNet was trained on general audio,
  not on your child. Expect the occasional miss and the occasional false alarm.

## Tests

```
python3 -m venv .venv && .venv/bin/pip install numpy requests
.venv/bin/python tests/test_core.py
.venv/bin/python tests/test_stream.py
```

40 tests, no microphone, camera, or network needed — every external call is
faked. They cover config validation (including refusing a public stream bind,
a weak password, and storm-inducing repeat intervals), the detection
heuristic, the full escalation ladder, the persistent re-alert loop (repeats,
acknowledgement stopping it, give-up behaviour, and Pushover expire sizing),
and the live view's authentication boundary.
