from __future__ import annotations

from collections import deque

import numpy as np

from ..types import SignalSample, VitalSigns


class RollingAverageEstimator:
    """
    占位估计器：
    - 不做真实频域分析；
    - 仅用窗口均值映射出一个可观测的心率值，验证管线。
    """

    def __init__(self, window_size: int = 150, min_samples: int = 30) -> None:
        self.window_size = window_size
        self.min_samples = min_samples
        self._buffer: deque[float] = deque(maxlen=window_size)

    def update(self, sample: SignalSample) -> VitalSigns | None:
        ppg = sample.values.get("ppg")
        if ppg is None:
            return None
        self._buffer.append(ppg)
        if len(self._buffer) < self.min_samples:
            return None

        avg = sum(self._buffer) / len(self._buffer)
        # 占位映射：后续替换为 FFT / Welch / 时频方法。
        hr = 60.0 + (avg - 0.5) * 80.0
        return VitalSigns(
            timestamp_s=sample.timestamp_s,
            heart_rate_bpm=hr,
            respiration_rate_bpm=None,
            confidence=min(1.0, len(self._buffer) / float(self.window_size)),
            debug={"buffer_size": len(self._buffer), "avg_ppg": avg},
        )


class FFTHeartRateEstimator:
    """
    基于频域分析的心率估计器：
    1) 维护滑动窗口信号；
    2) 去均值+线性去趋势；
    3) 加 Hann 窗后做 RFFT；
    4) 在心率频带内取主峰并转换为 BPM；
    5) 用 EMA 平滑输出，降低跳变。
    """

    def __init__(
        self,
        fps: float = 30.0,
        window_size: int = 300,
        min_samples: int = 150,
        hr_low_hz: float = 0.8,
        hr_high_hz: float = 3.0,
        smoothing_alpha: float = 0.9,
    ) -> None:
        if window_size <= 0:
            raise ValueError("window_size must be > 0")
        if min_samples <= 1:
            raise ValueError("min_samples must be > 1")
        if not (0.0 < hr_low_hz < hr_high_hz):
            raise ValueError("hr band is invalid")
        if fps <= 0:
            raise ValueError("fps must be > 0")
        if not (0.0 <= smoothing_alpha < 1.0):
            raise ValueError("smoothing_alpha must be in [0, 1)")

        self.fps = float(fps)
        self.window_size = window_size
        self.min_samples = min_samples
        self.hr_low_hz = hr_low_hz
        self.hr_high_hz = hr_high_hz
        self.smoothing_alpha = smoothing_alpha
        self._buffer: deque[float] = deque(maxlen=window_size)
        self._last_hr_bpm: float | None = None

    def update(self, sample: SignalSample) -> VitalSigns | None:
        ppg = sample.values.get("ppg")
        if ppg is None:
            return None
        self._buffer.append(float(ppg))
        if len(self._buffer) < self.min_samples:
            return None

        signal = np.asarray(self._buffer, dtype=np.float64)
        processed = self._preprocess(signal)

        spectrum = np.abs(np.fft.rfft(processed))
        freqs = np.fft.rfftfreq(processed.size, d=1.0 / self.fps)

        band_mask = (freqs >= self.hr_low_hz) & (freqs <= self.hr_high_hz)
        if not np.any(band_mask):
            return None

        band_freqs = freqs[band_mask]
        band_spec = spectrum[band_mask]
        if band_spec.size == 0:
            return None

        peak_idx = int(np.argmax(band_spec))
        peak_freq_hz = float(band_freqs[peak_idx])
        raw_hr_bpm = peak_freq_hz * 60.0

        if self._last_hr_bpm is None:
            smooth_hr_bpm = raw_hr_bpm
        else:
            a = self.smoothing_alpha
            smooth_hr_bpm = a * self._last_hr_bpm + (1.0 - a) * raw_hr_bpm
        self._last_hr_bpm = smooth_hr_bpm

        peak_power = float(band_spec[peak_idx])
        band_power = float(np.sum(band_spec) + 1e-12)
        # 将“主峰能量占比”映射到 [0,1] 的简单置信度。
        confidence = float(min(1.0, max(0.0, (peak_power / band_power) * 4.0)))

        return VitalSigns(
            timestamp_s=sample.timestamp_s,
            heart_rate_bpm=smooth_hr_bpm,
            respiration_rate_bpm=None,
            confidence=confidence,
            debug={
                "buffer_size": len(self._buffer),
                "peak_freq_hz": peak_freq_hz,
                "raw_hr_bpm": raw_hr_bpm,
                "band_power": band_power,
            },
        )

    @staticmethod
    def _preprocess(signal: np.ndarray) -> np.ndarray:
        centered = signal - np.mean(signal)
        n = centered.size
        x = np.arange(n, dtype=np.float64)
        # 线性去趋势，避免低频漂移影响频谱主峰。
        slope, intercept = np.polyfit(x, centered, deg=1)
        detrended = centered - (slope * x + intercept)
        windowed = detrended * np.hanning(n)
        return windowed

