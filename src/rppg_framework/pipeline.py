from __future__ import annotations

from dataclasses import dataclass

from .interfaces import FaceTracker, FrameSource, ResultSink, SignalExtractor, VitalEstimator
from .types import VitalSigns


@dataclass(slots=True)
class PipelineReport:
    processed_frames: int = 0
    tracking_failures: int = 0
    signal_failures: int = 0
    published_results: int = 0
    last_result: VitalSigns | None = None


class RPPGPipeline:
    """rPPG 主流程编排器。"""

    def __init__(
        self,
        source: FrameSource,
        face_tracker: FaceTracker,
        signal_extractor: SignalExtractor,
        estimator: VitalEstimator,
        sink: ResultSink,
        max_frames: int = 300,
        skip_failed_tracking: bool = True,
    ) -> None:
        self.source = source
        self.face_tracker = face_tracker
        self.signal_extractor = signal_extractor
        self.estimator = estimator
        self.sink = sink
        self.max_frames = max_frames
        self.skip_failed_tracking = skip_failed_tracking

    def run(self) -> PipelineReport:
        report = PipelineReport()
        for frame in self.source.frames():
            if report.processed_frames >= self.max_frames:
                break
            report.processed_frames += 1

            observation = self.face_tracker.track(frame)
            if observation is None or (not observation.tracking_ok and self.skip_failed_tracking):
                report.tracking_failures += 1
                continue

            sample = self.signal_extractor.extract(observation)
            if sample is None:
                report.signal_failures += 1
                continue

            result = self.estimator.update(sample)
            if result is None:
                continue

            self.sink.publish(result)
            report.published_results += 1
            report.last_result = result

        return report

