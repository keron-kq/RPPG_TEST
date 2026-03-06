from __future__ import annotations

from collections import deque

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

