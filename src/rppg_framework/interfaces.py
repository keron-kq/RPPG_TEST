from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from .types import FaceObservation, Frame, SignalSample, VitalSigns


class FrameSource(Protocol):
    def frames(self) -> Iterable[Frame]:
        """持续提供视频帧。"""


class FaceTracker(Protocol):
    def track(self, frame: Frame) -> FaceObservation | None:
        """检测并跟踪人脸，返回 ROI 与关键点信息。"""


class SignalExtractor(Protocol):
    def extract(self, observation: FaceObservation) -> SignalSample | None:
        """从 ROI 提取时序信号样本。"""


class VitalEstimator(Protocol):
    def update(self, sample: SignalSample) -> VitalSigns | None:
        """更新估计器状态并按需输出心率/呼吸率结果。"""


class ResultSink(Protocol):
    def publish(self, result: VitalSigns) -> None:
        """消费并输出结果（UI、日志、MQ、DB 等）。"""

