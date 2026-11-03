# Zynq-7020 实时 WORLD 语音处理 PS/PL 协同系统

本项目以 2026-10-30 的 Round30 板上版本为提交基线，面向全国大学生嵌入式芯片与系统设计竞赛 2026 AMD 自主选题初级组。系统在野火 Zynq-7020（`xc7z020clg400-2`）上运行 Linux/PetaLinux：ARM Cortex-A9 PS 执行 WORLD 音频流程、调度与 ALSA 输入输出，PL 中的 Vitis HLS 核加速固定 1024 点最小相位频谱计算，Linux coherent-DMA 驱动连接两侧数据通路。

## 最终实现

- 目标硬件：野火 Zynq-7020，`xc7z020clg400-2`。
- 运行系统：PetaLinux 2022.2；音频 codec 为 WM8960。
- 工具链：Vivado/Vitis HLS 2026.1。
- PS：WORLD 实时流、所选加速阶段以外的分析与合成、进程调度、ALSA 采集和播放。
- PL：WORLD 最小相位分析阶段的融合 HLS 核，输入 513 个 float32 对数频谱点，输出 513 个复数 float32 频点。
- 互连：AXI-Lite 控制映射和 coherent DMA，PL 数据主端口经 PS HP2 访问 DDR。
- 代码基准：`Pi-debug-cmd/2026_FPGA` 的 `PL-20261027-01` Round30 提交 `a8f6f8f32b159eaea277354118220c633f31fbc2`。

本项目呈现 PS 与 PL 对 WORLD 实时语音流程的协同实现。性能数据按实测条件列示，不将少量样本的墙钟差异作为性能收益结论。Round9 五项客观指标为 `0.5200 / 0.4719 / 0.0591 / 3.0789 / 0.1020`，Round10 主观音色和原始听感按项目验收记录通过；Round23 完成 20 秒有效实时语音运行；Round30 验证正常重启后候选自动启动、采集/播放 PCM 运行且 PL 调用计数递增。各证据分别对应不同验收环节，详见 `report/`。

本项目是 Linux/PetaLinux C++ PS 与 HLS PL 方案，不使用 PYNQ。AMD 指南第 3.3 节允许 RTL、Vitis HLS、PS 软件及组合实现；PYNQ 是初级组推荐方向，不是自主选题赛道的强制框架。

## 目录

| 路径 | 内容 |
| --- | --- |
| `src/hls/` | Round30 最小相位 HLS 核和 twiddle 常量 |
| `src/ps/` | WORLD 实时 PS 程序、PL 后端和 WORLD 版本源码 |
| `src/kernel/` | Linux coherent-DMA 驱动与接口头文件 |
| `src/rtl/` | Round30 Vivado 工程实际引用的 RTL 文件 |
| `build/` | HLS、Vivado、ARM 构建、校验和载荷脚本 |
| `board/` | 启动、安装、恢复、运行清单和野火原始音频工程包 |
| `sim/` | 固定向量 HLS 验证和启动故障检查 |
| `metrics/` | 指标汇总及校验脚本 |
| `report/` | 中文设计报告及 Round16、17、18、20、23、30 证据 |
| `docs/` | 架构、接口、硬件准备、协作记录与复现说明 |
| `skill/` | Vivado MCP、GitHub、DMA、黄金参考和 PS/PL 提示词工作流 |

目录和文件名按官方指南使用英文；中文说明放在文件正文中。

## 快速检查

在仓库根目录运行：

```sh
python -m unittest sim.test_world_minphase_boot -v
python metrics/scripts/validate_metrics.py
sh -n board/world_minphase_autostart.sh board/world_minphase_init.sh board/world_minphase_control.sh
```

HLS 固定向量验证使用 `sim/tb_world_minphase.cpp`，需 Vitis HLS 2026.1 和匹配的 WORLD 0.3.5 源码。ARM 程序使用 `build/build_world_minphase.ps1` 构建。完整工具、构建次序和外部运行环境见 [`docs/reproduction.md`](docs/reproduction.md)。

## 报告与交付

- 设计报告：[`report/DESIGN_REPORT.md`](report/DESIGN_REPORT.md)、[`report/design_report.pdf`](report/design_report.pdf) 和可编辑 Word 版 `report/design_report.docx`。
- 工程验收表：[`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md)。
- 指标索引：[`metrics/metrics.csv`](metrics/metrics.csv)。
- Round30 板端部署和重启记录：[`report/world_minphase_persistent_boot_round30_20261030.md`](report/world_minphase_persistent_boot_round30_20261030.md)。

生成的 Vivado 工程缓存、Round30 位流、运行镜像和可执行文件不放入源码归档；按复现说明在目标工具环境生成。仓库保留一份原始野火音频 Vivado 工程输入及其 SHA-256，见 `board/vendor_project/MANIFEST.md`；它不是 Round30 最终 XSA。PetaLinux SDK 从 [AMD 官方下载入口](https://www.amd.com/zh-cn/products/software/adaptive-socs-and-fpgas/embedded-software/petalinux-sdk.html) 获取。板端使用的基础系统为野火 PetaLinux 2022.2；系统镜像和受控真人音频不在公开仓库中。

## 许可证

项目自有代码按 MIT License 发布。WORLD 上游文件保留其原始许可证，分发时还需遵循板卡厂商 IP 与第三方依赖各自的许可条款。
