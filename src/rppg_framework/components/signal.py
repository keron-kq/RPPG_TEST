from __future__ import annotations

from ..types import FaceObservation, SignalSample


class GreenChannelSignalExtractor:
    """绿色通道占位提取器。"""

    def __init__(self, field_name: str = "green") -> None:
        self.field_name = field_name

    def extract(self, observation: FaceObservation) -> SignalSample | None:
        if not observation.rois:
            return None
        first_roi = observation.rois[0]
        payload = first_roi.payload
        if not isinstance(payload, dict):
            return None
        green = payload.get(self.field_name)
        if green is None:
            return None
        return SignalSample(timestamp_s=observation.frame.timestamp_s, values={"ppg": float(green)})

