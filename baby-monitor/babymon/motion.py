"""Webcam motion detection and frame supply for the private live view.

One camera handle is opened here and shared: the motion detector and the
stream server both read from this object, because macOS will not let two
processes grab the same camera. Frames live in a single-slot buffer that is
overwritten ~6 times a second. They are never written to disk.
"""

from __future__ import annotations

import logging
import threading
import time

import numpy as np

log = logging.getLogger("babymon.motion")


class Camera:
    """Owns the webcam, computes motion, and hands out the latest frame."""

    def __init__(self, cfg, width: int = 640):
        self.cfg = cfg
        self.width = width
        self._cap = None
        self._frame = None            # latest BGR frame, for the stream
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._prev_gray = None
        self._motion_since: float | None = None
        self.last_ratio: float = 0.0
        self.available = False

    def start(self) -> None:
        try:
            import cv2
        except Exception as exc:
            log.error(
                "OpenCV is not available (%s) -- motion detection and live view "
                "are disabled. Audio alerting is unaffected.", exc,
            )
            return

        try:
            cap = cv2.VideoCapture(self.cfg.camera_index)
        except Exception as exc:
            log.error("camera %d failed to open (%s); continuing audio-only",
                      self.cfg.camera_index, exc)
            return
        if not cap.isOpened():
            log.error(
                "could not open camera index %d -- motion detection and live view "
                "are disabled. Audio alerting is unaffected.",
                self.cfg.camera_index,
            )
            return
        self._cap = cap
        self.available = True
        threading.Thread(target=self._loop, name="camera", daemon=True).start()
        log.info("camera %d open", self.cfg.camera_index)

    def stop(self) -> None:
        self._stop.set()
        if self._cap is not None:
            try:
                self._cap.release()
            except Exception:
                pass

    def _loop(self) -> None:
        import cv2

        interval = 1.0 / 10.0
        failures = 0
        while not self._stop.wait(interval):
            try:
                ok, frame = self._cap.read()
            except Exception:
                ok, frame = False, None
            if not ok:
                failures += 1
                if failures == 50:   # ~5s of nothing
                    log.warning("camera stopped returning frames; still listening on audio")
                    self.available = False
                continue
            if failures:
                if not self.available:
                    log.info("camera recovered")
                self.available = True
                failures = 0

            h, w = frame.shape[:2]
            if w > self.width:
                frame = cv2.resize(frame, (self.width, int(h * self.width / w)))

            with self._lock:
                self._frame = frame

            gray = cv2.GaussianBlur(
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (21, 21), 0
            )
            if self._prev_gray is None:
                self._prev_gray = gray
                continue

            delta = cv2.absdiff(self._prev_gray, gray)
            thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
            ratio = float(np.count_nonzero(thresh)) / thresh.size
            self.last_ratio = ratio
            self._prev_gray = gray

            if ratio >= self.cfg.sensitivity:
                if self._motion_since is None:
                    self._motion_since = time.time()
            else:
                self._motion_since = None

    def latest_frame(self):
        with self._lock:
            return None if self._frame is None else self._frame.copy()

    def moving(self) -> tuple[bool, float]:
        """True once motion has been continuous for the configured duration."""
        if not self.cfg.enabled or self._motion_since is None:
            return False, self.last_ratio
        held = time.time() - self._motion_since
        return held >= self.cfg.sustain_seconds, self.last_ratio
