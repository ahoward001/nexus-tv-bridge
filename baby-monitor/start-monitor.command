#!/bin/bash
# Double-click to start BabyMon in this window. Close the window to stop.
# Use this rather than the login item if macOS is refusing mic/camera access
# to the background service -- permissions granted here stick to Terminal.
exec "$HOME/Library/Application Support/BabyMon/bin/babymon" run
