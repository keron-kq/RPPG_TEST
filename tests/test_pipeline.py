from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from rppg_framework.cli import build_pipeline
from rppg_framework.config import AppConfig


class PipelineSmokeTest(unittest.TestCase):
    def test_pipeline_runs_and_publishes_results(self) -> None:
        cfg = AppConfig.from_dict(
            {
                "pipeline": {"max_frames": 80, "skip_failed_tracking": True},
                "source_params": {"fps": 30, "total_frames": 100},
                "estimator_params": {"window_size": 60, "min_samples": 10},
            }
        )
        pipeline = build_pipeline(cfg)
        report = pipeline.run()
        self.assertGreater(report.processed_frames, 0)
        self.assertGreater(report.published_results, 0)
        self.assertIsNotNone(report.last_result)

    def test_config_from_file(self) -> None:
        raw = {
            "components": {"source": "dummy"},
            "pipeline": {"max_frames": 10},
            "source_params": {"fps": 10, "total_frames": 20},
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cfg.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            cfg = AppConfig.from_file(path)
        self.assertEqual(cfg.components.source, "dummy")
        self.assertEqual(cfg.pipeline.max_frames, 10)
        self.assertEqual(cfg.source_params["fps"], 10)


if __name__ == "__main__":
    unittest.main()

