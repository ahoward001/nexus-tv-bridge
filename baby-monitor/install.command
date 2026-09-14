#!/bin/bash
# BabyMon installer for macOS. Double-click this file in Finder.
set -uo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP="$HOME/Library/Application Support/BabyMon"
VENV="$APP/venv"
CFG_DIR="$HOME/.config/babymon"
CFG="$CFG_DIR/config.toml"
AGENT="$HOME/Library/LaunchAgents/com.babymon.monitor.plist"
BIN="$APP/bin"

bold(){ printf "\033[1m%s\033[0m\n" "$*"; }
ok(){   printf "  \033[32m✓\033[0m %s\n" "$*"; }
warn(){ printf "  \033[33m!\033[0m %s\n" "$*"; }
die(){  printf "\n\033[31m✗ %s\033[0m\n\n" "$*"; echo "Press return to close."; read -r; exit 1; }
ask(){ # ask VAR "prompt" -> echoes answer
  local __v="$1"; shift
  printf "%s " "$*" >&2
  read -r __a
  printf '%s' "$__a"
}

clear
bold "BabyMon setup"
echo "Everything installs into your own user folder. Nothing runs as admin."
echo

# ---------------------------------------------------------------- python ---
bold "1. Python"
PY="$(command -v python3 || true)"
if [ -z "$PY" ]; then
  die "python3 isn't installed. Run 'xcode-select --install' in Terminal, then re-run this installer."
fi
PYV="$("$PY" -c 'import sys;print("%d.%d"%sys.version_info[:2])')"
case "$PYV" in
  3.9|3.10|3.11|3.12) ok "python $PYV" ;;
  *) warn "python $PYV is untested (3.9-3.12 are known good); continuing" ;;
esac

# ------------------------------------------------------------------ venv ---
bold "2. Dependencies"
mkdir -p "$APP" "$BIN" "$CFG_DIR" || die "could not create $APP"
if [ ! -d "$VENV" ]; then
  "$PY" -m venv "$VENV" || die "could not create the virtual environment"
fi
"$VENV/bin/python" -m pip install --quiet --upgrade pip wheel >/dev/null 2>&1

echo "  installing (this takes a couple of minutes the first time)…"
if "$VENV/bin/python" -m pip install --quiet -r "$SRC/requirements.txt"; then
  ok "all dependencies installed"
else
  warn "the full install failed -- retrying without the ML classifier"
  grep -v '^mediapipe' "$SRC/requirements.txt" > "$APP/req-min.txt"
  "$VENV/bin/python" -m pip install --quiet -r "$APP/req-min.txt" \
    || die "dependency install failed. Send the output above to whoever set this up."
  warn "cry detection will use the simpler energy fallback (more false alarms)"
fi

# Install the package itself so `babymon` works from anywhere.
cp -R "$SRC/babymon" "$APP/babymon"
cp -R "$SRC/scripts" "$APP/scripts"
cat > "$BIN/babymon" <<EOF
#!/bin/bash
cd "$APP" && exec "$VENV/bin/python" -m babymon.main "\$@"
EOF
chmod +x "$BIN/babymon"
ok "installed to $APP"

# ----------------------------------------------------------------- model ---
bold "3. Cry-detection model"
"$VENV/bin/python" "$APP/scripts/fetch_model.py" "$APP/models/yamnet.tflite" \
  && ok "model ready" || warn "model download failed -- falling back to energy detection"

# ---------------------------------------------------------------- config ---
bold "4. Configuration"
if [ -f "$CFG" ]; then
  ok "keeping your existing config at $CFG"
else
  cp "$SRC/config.example.toml" "$CFG"

  TOPIC="babymon-$("$VENV/bin/python" -c 'import secrets;print(secrets.token_urlsafe(18))')"
  STREAMPW="$("$VENV/bin/python" -c 'import secrets;print(secrets.token_urlsafe(14))')"
  "$VENV/bin/python" - "$CFG" "$TOPIC" "$STREAMPW" <<'PYEOF'
import re, sys
path, topic, pw = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(path).read()
s = s.replace('topic = ""', f'topic = "{topic}"', 1)
s = s.replace('password = ""', f'password = "{pw}"', 1)
open(path, 'w').write(s)
PYEOF
  chmod 600 "$CFG"
  ok "config written to $CFG (readable only by you)"
  echo
  echo "  Your free ntfy alert topic is:"
  printf "      \033[1m%s\033[0m\n" "$TOPIC"
  echo "  Install the 'ntfy' app on your phone and subscribe to exactly that."
  echo "  Treat it like a password -- anyone who knows it sees your alerts."
  echo
  echo "  Your live-view password is:"
  printf "      \033[1m%s\033[0m\n" "$STREAMPW"
  echo

  echo "  Pushover gives you a siren that repeats until you acknowledge it."
  echo "  Leave blank to skip (you can add it later by editing the config)."
  PO_USER="$(ask x '    Pushover user key:')"
  if [ -n "$PO_USER" ]; then
    PO_TOKEN="$(ask x '    Pushover API token:')"
    "$VENV/bin/python" - "$CFG" "$PO_USER" "$PO_TOKEN" <<'PYEOF'
import sys
path, user, token = sys.argv[1:4]
s = open(path).read()
s = s.split('[alerts.pushover]')
s[1] = s[1].replace('enabled = false', 'enabled = true', 1)
s[1] = s[1].replace('user_key = ""', f'user_key = "{user}"', 1)
s[1] = s[1].replace('api_token = ""', f'api_token = "{token}"', 1)
open(path, 'w').write('[alerts.pushover]'.join(s))
PYEOF
    ok "Pushover enabled"
  fi

  echo
  echo "  Twilio makes your phone actually ring if you don't acknowledge."
  echo "  Leave blank to skip."
  TW_SID="$(ask x '    Twilio Account SID:')"
  if [ -n "$TW_SID" ]; then
    TW_TOK="$(ask x '    Twilio Auth Token:')"
    TW_FROM="$(ask x '    Your Twilio number (+15551234567):')"
    TW_TO="$(ask x '    Your cell number   (+15559876543):')"
    "$VENV/bin/python" - "$CFG" "$TW_SID" "$TW_TOK" "$TW_FROM" "$TW_TO" <<'PYEOF'
import sys
path, sid, tok, frm, to = sys.argv[1:6]
s = open(path).read().split('[alerts.twilio]')
s[1] = s[1].replace('enabled = false', 'enabled = true', 1)
s[1] = s[1].replace('account_sid = ""', f'account_sid = "{sid}"', 1)
s[1] = s[1].replace('auth_token = ""', f'auth_token = "{tok}"', 1)
s[1] = s[1].replace('from_number = ""', f'from_number = "{frm}"', 1)
s[1] = s[1].replace('to_number = ""', f'to_number = "{to}"', 1)
open(path, 'w').write('[alerts.twilio]'.join(s))
PYEOF
    ok "Twilio enabled"
    echo
    warn "On iPhone: save $TW_FROM as a contact, then Edit > Ringtone >"
    warn "Emergency Bypass ON. That's what makes it ring through silent mode."
  fi
  chmod 600 "$CFG"
fi

# ----------------------------------------------------------- permissions ---
bold "5. macOS permissions"
echo "  macOS will now ask for microphone and camera access. Click Allow on both."
echo "  (If no dialog appears, grant them under System Settings > Privacy & Security.)"
echo
"$BIN/babymon" devices 2>/dev/null | sed 's/^/  /'

# ------------------------------------------------------------ test alert ---
bold "6. Test alert"
echo "  Sending a test to every channel you configured…"
"$BIN/babymon" test 2>&1 | sed 's/^/  /'

# ------------------------------------------------------------ launchagent --
bold "7. Start automatically at login"
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$AGENT" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.babymon.monitor</string>
  <key>ProgramArguments</key>
  <array><string>$BIN/babymon</string><string>run</string></array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>ProcessType</key><string>Interactive</string>
  <key>StandardOutPath</key><string>$APP/launchd.out.log</string>
  <key>StandardErrorPath</key><string>$APP/launchd.err.log</string>
</dict></plist>
EOF
launchctl unload "$AGENT" 2>/dev/null
if launchctl load "$AGENT" 2>/dev/null; then
  ok "BabyMon will start automatically at login"
else
  warn "couldn't register the login item -- use start-monitor.command instead"
fi

# ----------------------------------------------------------------- done ----
echo
bold "Done."
"$BIN/babymon" doctor 2>&1 | sed 's/^/  /'
echo
echo "  Start it now:   double-click start-monitor.command"
echo "  Check on it:    $BIN/babymon doctor"
echo "  Logs:           $APP/babymon.log"
echo
echo "Press return to close."
read -r
