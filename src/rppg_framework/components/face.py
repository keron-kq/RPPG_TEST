from __future__ import annotations

from ..types import FaceObservation, Frame, ROI


class SimpleFaceTracker:
    """
    人脸跟踪占位实现。
    后续可替换为 Dlib / MediaPipe / 自研关键点模型。
    """

    def __init__(self, enable_tracking: bool = True) -> None:
        self.enable_tracking = enable_tracking

    def track(self, frame: Frame) -> FaceObservation | None:
        if not self.enable_tracking:
            return None
        rois = [
            ROI(name="forehead", bbox_xywh=(100, 50, 120, 60), payload=frame.payload),
            ROI(name="left_cheek", bbox_xywh=(80, 120, 90, 70), payload=frame.payload),
            ROI(name="right_cheek", bbox_xywh=(180, 120, 90, 70), payload=frame.payload),
        ]
        return FaceObservation(frame=frame, landmarks=[], rois=rois, tracking_ok=True)

