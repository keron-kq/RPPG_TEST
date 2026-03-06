from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ComponentsConfig:
    source: str = "dummy"
    face_tracker: str = "simple"
    signal_extractor: str = "green_channel"
    estimator: str = "rolling_average"
    sink: str = "console"


@dataclass(slots=True)
class PipelineConfig:
    max_frames: int = 300
    skip_failed_tracking: bool = True


@dataclass(slots=True)
class AppConfig:
    components: ComponentsConfig = field(default_factory=ComponentsConfig)
    pipeline: PipelineConfig = field(default_factory=PipelineConfig)
    source_params: dict[str, Any] = field(default_factory=lambda: {"fps": 30, "total_frames": 300})
    face_tracker_params: dict[str, Any] = field(default_factory=dict)
    signal_extractor_params: dict[str, Any] = field(default_factory=dict)
    estimator_params: dict[str, Any] = field(default_factory=lambda: {"window_size": 150, "min_samples": 30})
    sink_params: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_file(cls, path: str | Path) -> "AppConfig":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(raw)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "AppConfig":
        components = ComponentsConfig(**raw.get("components", {}))
        pipeline = PipelineConfig(**raw.get("pipeline", {}))
        return cls(
            components=components,
            pipeline=pipeline,
            source_params=raw.get("source_params", {"fps": 30, "total_frames": 300}),
            face_tracker_params=raw.get("face_tracker_params", {}),
            signal_extractor_params=raw.get("signal_extractor_params", {}),
            estimator_params=raw.get("estimator_params", {"window_size": 150, "min_samples": 30}),
            sink_params=raw.get("sink_params", {}),
        )

