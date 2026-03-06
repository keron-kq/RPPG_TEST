from __future__ import annotations

import math
import time
from collections.abc import Iterable

from ..types import Frame


class DummyFrameSource:
    """生成模拟视频帧，用于验证流程连通性。"""

    def __init__(self, fps: int = 30, total_frames: int = 300) -> None:
        self.fps = fps
        self.total_frames = total_frames

    def frames(self) -> Iterable[Frame]:
        t0 = time.monotonic()
        for idx in range(self.total_frames):
            ts = idx / self.fps
            # 通过正弦波构造一个可重复的“绿色通道”模拟脉搏信号
            green_value = 0.5 + 0.08 * math.sin(2.0 * math.pi * 1.2 * ts)
            payload = {"green": green_value}
            yield Frame(index=idx, timestamp_s=time.monotonic() - t0, payload=payload)

