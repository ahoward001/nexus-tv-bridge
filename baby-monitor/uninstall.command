#!/bin/bash
# Removes BabyMon. Your config (with API keys) is left in place unless you
# say otherwise, so reinstalling doesn't mean re-entering everything.
set -uo pipefail
APP="$HOME/Library/Application Support/BabyMon"
AGENT="$HOME/Library/LaunchAgents/com.babymon.monitor.plist"
CFG="$HOME/.config/babymon/config.toml"

echo "Stopping and removing BabyMon…"
launchctl unload "$AGENT" 2>/dev/null
rm -f "$AGENT"
rm -rf "$APP"
echo "Removed the app and login item."

printf "Also delete your config and API keys at %s? [y/N] " "$CFG"
read -r a
case "$a" in
  y|Y) rm -f "$CFG"; echo "Config deleted." ;;
  *)   echo "Config kept." ;;
esac
echo "Press return to close."; read -r
