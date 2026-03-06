# rPPG 二次开发框架（Skeleton）

该仓库现已初始化为一个可扩展的 Python 工程骨架，目标是：

- 先跑通 **采集 -> 人脸/ROI -> 信号提取 -> 生理指标估计 -> 输出** 的主流程；
- 后续你可以仅替换算法实现，不需要重搭工程。

## 目录结构

```text
.
├── configs/
│   └── default.json
├── src/
│   └── rppg_framework/
│       ├── cli.py
│       ├── config.py
│       ├── factories.py
│       ├── interfaces.py
│       ├── pipeline.py
│       ├── types.py
│       └── components/
│           ├── estimation.py
│           ├── face.py
│           ├── signal.py
│           ├── sinks.py
│           └── sources.py
└── tests/
    └── test_pipeline.py
```

## 快速开始

```bash
python -m pip install -e .
rppg --config configs/default.json
```

## 如何做算法二开

1. 在 `interfaces.py` 查看抽象接口定义；
2. 在 `components/` 下新增你自己的实现类（比如 `MyFaceTracker`）；
3. 在 `factories.py` 注册组件名到实现类；
4. 在 `configs/default.json` 中切换组件名和参数；
5. 运行 `rppg --config ...` 验证流程。

## 当前默认实现说明

默认组件包含一个可直接用于频域心率估计的基础实现：

- `DummyFrameSource`：生成模拟帧；
- `SimpleFaceTracker`：模拟 ROI 追踪；
- `GreenChannelSignalExtractor`：提取绿色通道值；
- `FFTHeartRateEstimator`：基于去趋势 + FFT + 频带主峰的心率估计；
- `ConsoleSink`：控制台输出。

当前实现可用于基础链路验证和初步调参，后续可替换为更完整的滤波、峰值置信度融合与呼吸频率估计逻辑。

