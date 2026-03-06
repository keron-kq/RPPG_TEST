from __future__ import annotations

from ..types import VitalSigns


class ConsoleSink:
    """结果打印占位实现。"""

    def __init__(self, prefix: str = "[rPPG]") -> None:
        self.prefix = prefix

    def publish(self, result: VitalSigns) -> None:
        hr = "N/A" if result.heart_rate_bpm is None else f"{result.heart_rate_bpm:.2f}"
        rr = "N/A" if result.respiration_rate_bpm is None else f"{result.respiration_rate_bpm:.2f}"
        print(
            f"{self.prefix} t={result.timestamp_s:.2f}s, "
            f"HR={hr} bpm, RR={rr} bpm, conf={result.confidence:.2f}"
        )

