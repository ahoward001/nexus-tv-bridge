"""Cry detection.

Two backends:

  mediapipe -- Google's YAMNet audio event classifier running locally via
               TensorFlow Lite. It has dedicated classes for infant crying,
               so it distinguishes a baby from a slammed door or a truck.
               This is the one you want.

  energy    -- No-ML fallback for when mediapipe won't install. Tracks the
               room's noise floor and fires on sustained loud sound whose
               energy sits in the band where infant cries live. Cruder, more
               false alarms, but it works everywhere.

Audio is held in a short rolling buffer in RAM and overwritten continuously.
Nothing is recorded, saved, or transmitted.
"""

from __future__ import annotations

import collections
import logging
import threading
import time
from dataclasses import dataclass

import numpy as np

log = logging.getLogger("babymon.detector")

SAMPLE_RATE = 16_000          # YAMNet requires 16 kHz mono
BLOCK_SECONDS = 0.5           # how often we score
WINDOW_SECONDS = 1.0          # audio fed to the classifier (YAMNet needs >=0.975s)
_BLOCK = int(SAMPLE_RATE * BLOCK_SECONDS)
_WINDOW = int(SAMPLE_RATE * WINDOW_SECONDS)


@dataclass
class Score:
    at: float
    value: float          # 0..1 confidence this is a distressed baby
    label: str            # which class won, for the log / notification text


class _Backend:
    name = "base"

    def score(self, window: np.ndarray) -> Score:
        raise NotImplementedError

    def close(self) -> None:
        pass


class MediapipeBackend(_Backend):
    name = "mediapipe"

    def __init__(self, model_path: str, watch_classes: list[str]):
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import audio as mp_audio
        from mediapipe.tasks.python.components import containers

        self._containers = containers
        opts = mp_audio.AudioClassifierOptions(
            base_options=mp_python.BaseOptions(model_asset_path=model_path),
            max_results=8,
        )
        self._clf = mp_audio.AudioClassifier.create_from_options(opts)
        # Match case-insensitively; YAMNet's class names are fixed strings but
        # a typo in someone's config shouldn't silently disable detection.
        self._watch = {c.strip().lower() for c in watch_classes}
        log.info("cry detector: YAMNet via mediapipe, watching %d classes", len(self._watch))

    def score(self, window: np.ndarray) -> Score:
        clip = self._containers.AudioData.create_from_array(
            window.astype(np.float32), SAMPLE_RATE
        )
        results = self._clf.classify(clip)
        best, label = 0.0, ""
        for res in results:
            if not res.classifications:
                continue
            for cat in res.classifications[0].categories:
                nm = (cat.category_name or "").strip().lower()
                if nm in self._watch and cat.score > best:
                    best, label = float(cat.score), cat.category_name
        return Score(time.time(), best, label or "baby cry")

    def close(self) -> None:
        try:
            self._clf.close()
        except Exception:
            pass


class EnergyBackend(_Backend):
    """Adaptive loudness + band-ratio heuristic.

    Infant cries are loud relative to a quiet nursery and concentrate their
    energy roughly 300 Hz - 3 kHz. We track a rolling noise floor so the
    detector calibrates itself to the room instead of using a fixed dB value
    that would be wrong in every house.
    """

    name = "energy"
    _LO_HZ, _HI_HZ = 300.0, 3000.0

    def __init__(self) -> None:
        self._floor = collections.deque(maxlen=600)  # ~5 min of 0.5s blocks
        log.warning(
            "cry detector: using the ENERGY fallback (mediapipe unavailable). "
            "Expect more false alarms than the YAMNet backend."
        )

    def score(self, window: np.ndarray) -> Score:
        rms = float(np.sqrt(np.mean(np.square(window))) + 1e-9)
        self._floor.append(rms)

        # 20th percentile of recent RMS ~= the room at rest.
        floor = float(np.percentile(self._floor, 20)) if len(self._floor) > 20 else rms
        loudness = rms / max(floor, 1e-6)

        spec = np.abs(np.fft.rfft(window * np.hanning(len(window))))
        freqs = np.fft.rfftfreq(len(window), 1.0 / SAMPLE_RATE)
        band = spec[(freqs >= self._LO_HZ) & (freqs <= self._HI_HZ)].sum()
        ratio = float(band / (spec.sum() + 1e-9))

        # Loud (>=6x the noise floor) AND tonally in the cry band.
        loud_term = np.clip((loudness - 3.0) / 9.0, 0.0, 1.0)
        band_term = np.clip((ratio - 0.35) / 0.35, 0.0, 1.0)
        return Score(time.time(), float(loud_term * band_term), "loud crying sound")


def build_backend(cfg, model_path: str) -> _Backend:
    want = cfg.backend
    if want in ("auto", "mediapipe"):
        try:
            return MediapipeBackend(model_path, cfg.watch_classes)
        except Exception as exc:
            if want == "mediapipe":
                raise RuntimeError(
                    f"detect.backend is pinned to 'mediapipe' but it failed to load: "
                    f"{exc}\nSet backend = \"auto\" to fall back automatically."
                ) from exc
            log.warning("mediapipe backend unavailable (%s); falling back to energy", exc)
    return EnergyBackend()


class CryDetector:
    """Listens on the microphone and reports sustained infant distress."""

    def __init__(self, cfg, model_path: str):
        self.cfg = cfg
        self._backend = build_backend(cfg, model_path)
        self._scores: collections.deque[Score] = collections.deque(maxlen=240)
        self._buf = np.zeros(_WINDOW, dtype=np.float32)
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._stream = None
        self.last_score: float = 0.0
        self.last_label: str = ""
        self.backend_name: str = self._backend.name

    # -- lifecycle ---------------------------------------------------------

    def start(self) -> None:
        import sounddevice as sd

        device = self.cfg.input_device or None
        if device:
            log.info("microphone: %s", device)

        def _cb(indata, frames, time_info, status):
            if status:
                log.debug("audio status: %s", status)
            mono = indata[:, 0] if indata.ndim > 1 else indata
            with self._lock:
                n = len(mono)
                if n >= _WINDOW:
                    self._buf[:] = mono[-_WINDOW:]
                else:
                    self._buf[:-n] = self._buf[n:]
                    self._buf[-n:] = mono

        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=_BLOCK,
            device=device,
            callback=_cb,
        )
        self._stream.start()
        threading.Thread(target=self._loop, name="cry-scorer", daemon=True).start()
        log.info("listening (backend=%s)", self._backend.name)

    def stop(self) -> None:
        self._stop.set()
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
        self._backend.close()

    # -- scoring -----------------------------------------------------------

    def _loop(self) -> None:
        while not self._stop.wait(BLOCK_SECONDS):
            with self._lock:
                window = self._buf.copy()
            # All-zero buffer means the mic isn't delivering audio yet.
            if not np.any(window):
                continue
            try:
                s = self._backend.score(window)
            except Exception:
                log.exception("scoring failed; skipping this block")
                continue
            self._scores.append(s)
            self.last_score, self.last_label = s.value, s.label

    def crying(self) -> tuple[bool, float, str]:
        """True when the cry score has held above threshold long enough.

        Requires 60% of the blocks in the sustain window to be over threshold,
        so a brief dip (a baby drawing breath between wails) doesn't reset it,
        but a single isolated bang cannot trip it either.
        """
        cutoff = time.time() - self.cfg.sustain_seconds
        recent = [s for s in self._scores if s.at >= cutoff]
        needed = max(2, int(self.cfg.sustain_seconds / BLOCK_SECONDS * 0.6))
        if len(recent) < needed:
            return False, self.last_score, self.last_label
        hits = [s for s in recent if s.value >= self.cfg.cry_threshold]
        if len(hits) < needed:
            return False, self.last_score, self.last_label
        peak = max(hits, key=lambda s: s.value)
        return True, peak.value, peak.label
