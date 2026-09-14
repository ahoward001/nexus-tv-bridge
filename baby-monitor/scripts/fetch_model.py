#!/usr/bin/env python3
"""Download the YAMNet cry-classification model.

Source is Google's MediaPipe model CDN -- a plain public HTTPS file, no
account and no API key. The model runs entirely on your laptop; downloading
it is the only time anything is fetched.
"""

from __future__ import annotations

import hashlib
import sys
import urllib.request
from pathlib import Path

URL = "https://storage.googleapis.com/mediapipe-models/audio_classifier/yamnet/float32/1/yamnet.tflite"
MIN_BYTES = 3_000_000  # the real file is ~4.1 MB; anything smaller is an error page


def main() -> int:
    dest = Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else Path.home() / "Library/Application Support/BabyMon/models/yamnet.tflite"
    ).expanduser()
    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists() and dest.stat().st_size >= MIN_BYTES:
        print(f"Model already present ({dest.stat().st_size:,} bytes)")
        return 0

    print(f"Downloading cry-detection model -> {dest}")
    tmp = dest.with_suffix(".part")
    try:
        with urllib.request.urlopen(URL, timeout=120) as r, tmp.open("wb") as fh:
            data = r.read()
            fh.write(data)
    except Exception as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        tmp.unlink(missing_ok=True)
        return 1

    if len(data) < MIN_BYTES:
        print(f"Download looks wrong ({len(data)} bytes). Not installing.", file=sys.stderr)
        tmp.unlink(missing_ok=True)
        return 1

    tmp.replace(dest)
    print(f"Done: {len(data):,} bytes, sha256 {hashlib.sha256(data).hexdigest()[:16]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
