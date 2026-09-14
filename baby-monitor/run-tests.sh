#!/bin/bash
# Run the offline test suite. No hardware or network required.
set -e
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
if [ ! -d .venv ]; then
  "$PY" -m venv .venv
  .venv/bin/pip install -q numpy requests
fi
.venv/bin/python tests/test_core.py "$@"
.venv/bin/python tests/test_stream.py "$@"
