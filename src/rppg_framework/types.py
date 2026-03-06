from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Frame:
    """单帧数据容器。"""

    index: int
    timestamp_s: float
    payload: Any


@dataclass(slots=True)
class ROI:
    """感兴趣区域（ROI）描述。"""

    name: str
    bbox_xywh: tuple[int, int, int, int] | None = None
    payload: Any = None


@dataclass(slots=True)
class FaceObservation:
    """人脸跟踪阶段输出。"""

    frame: Frame
    landmarks: list[tuple[float, float]] = field(default_factory=list)
    rois: list[ROI] = field(default_factory=list)
    tracking_ok: bool = True


@dataclass(slots=True)
class SignalSample:
    """信号样本。"""

    timestamp_s: float
    values: dict[str, float]


@dataclass(slots=True)
class VitalSigns:
    """估计输出。"""

    timestamp_s: float
    heart_rate_bpm: float | None = None
    respiration_rate_bpm: float | None = None
    confidence: float = 0.0
    debug: dict[str, Any] = field(default_factory=dict)

