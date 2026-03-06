from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .components.estimation import FFTHeartRateEstimator, RollingAverageEstimator
from .components.face import SimpleFaceTracker
from .components.signal import GreenChannelSignalExtractor
from .components.sinks import ConsoleSink
from .components.sources import DummyFrameSource

Builder = Callable[..., Any]


class ComponentFactory:
    def __init__(self) -> None:
        self._source_builders: dict[str, Builder] = {
            "dummy": DummyFrameSource,
        }
        self._face_tracker_builders: dict[str, Builder] = {
            "simple": SimpleFaceTracker,
        }
        self._signal_builders: dict[str, Builder] = {
            "green_channel": GreenChannelSignalExtractor,
        }
        self._estimator_builders: dict[str, Builder] = {
            "rolling_average": RollingAverageEstimator,
            "fft_hr": FFTHeartRateEstimator,
        }
        self._sink_builders: dict[str, Builder] = {
            "console": ConsoleSink,
        }

    def create_source(self, name: str, **kwargs: Any) -> Any:
        return self._source_builders[name](**kwargs)

    def create_face_tracker(self, name: str, **kwargs: Any) -> Any:
        return self._face_tracker_builders[name](**kwargs)

    def create_signal_extractor(self, name: str, **kwargs: Any) -> Any:
        return self._signal_builders[name](**kwargs)

    def create_estimator(self, name: str, **kwargs: Any) -> Any:
        return self._estimator_builders[name](**kwargs)

    def create_sink(self, name: str, **kwargs: Any) -> Any:
        return self._sink_builders[name](**kwargs)

