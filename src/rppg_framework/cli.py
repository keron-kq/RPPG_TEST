from __future__ import annotations

import argparse

from .config import AppConfig
from .factories import ComponentFactory
from .pipeline import RPPGPipeline


def build_pipeline(config: AppConfig) -> RPPGPipeline:
    factory = ComponentFactory()
    source = factory.create_source(config.components.source, **config.source_params)
    face_tracker = factory.create_face_tracker(config.components.face_tracker, **config.face_tracker_params)
    signal_extractor = factory.create_signal_extractor(
        config.components.signal_extractor, **config.signal_extractor_params
    )
    estimator = factory.create_estimator(config.components.estimator, **config.estimator_params)
    sink = factory.create_sink(config.components.sink, **config.sink_params)
    return RPPGPipeline(
        source=source,
        face_tracker=face_tracker,
        signal_extractor=signal_extractor,
        estimator=estimator,
        sink=sink,
        max_frames=config.pipeline.max_frames,
        skip_failed_tracking=config.pipeline.skip_failed_tracking,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="rPPG framework runner")
    parser.add_argument("--config", default="configs/default.json", help="配置文件路径（JSON）")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = AppConfig.from_file(args.config)
    pipeline = build_pipeline(config)
    report = pipeline.run()
    print(
        "[rPPG] finished:",
        f"frames={report.processed_frames},",
        f"tracking_failures={report.tracking_failures},",
        f"signal_failures={report.signal_failures},",
        f"published={report.published_results}",
    )


if __name__ == "__main__":
    main()

