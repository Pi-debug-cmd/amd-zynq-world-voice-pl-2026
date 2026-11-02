# Zynq-7020 上的 WORLD 最小相位 PS+PL 项目

本项目是面向 AMD FPGA 自主命题赛道的实时 WORLD 语音处理项目。可编程逻辑（PL）加速 WORLD 中固定 1024 点的最小相位频谱处理阶段；ARM 处理系统（PS）运行其余 WORLD 分析、流调度和音频输入输出。

## 项目状态

这是 Round30 实现的源代码与证据包。用户确认 Round9 的五项离线客观指标基本通过、原始 Round10 听感通过，并接受已有 Round23/30 板端证据作为稳定性和延迟验收依据。Round24 没有有效语音，因此不纳入该结论。项目的主要技术点是 PS/PL 协作：ARM PS 运行 WORLD 流程和音频链路，HLS 加速器通过 DMA 接口在 PL 中执行选定的最小相位阶段。本项目没有声称整个 WORLD 流程都运行在 PL 中。详见[设计报告](report/DESIGN_REPORT.md)和[提交清单](report/SUBMISSION_CHECKLIST.md)。

GitHub Release `round30-submission-20261101-v4` 包含对应的 Round30 板端载荷、`.bit`、`.hwh`、`.xsa`、精简 Vivado 源码包、完整 `archive_project` Vivado 源码包及布线实现报告。两个源码包均已解压到干净目录，并在 Vivado 2026.1 中打开；其中的 Zynq Block Design 均通过验证。完整源码包包含生成的 IP 源码，但不含综合/实现运行输出，因此不声称已完成全流程布线重建。PetaLinux 镜像仍待补齐。SHA-256 和来源信息见[制品清单](board/artifacts/round30/MANIFEST.md)。

## 平台与实现

- Board: Wildfire Zynq-7020, device `xc7z020clg400-2`.
- 工具链：Vivado/Vitis 2026.1；板端运行 Linux PetaLinux。
- 软硬件划分：PS 运行 C++ WORLD 流处理程序并处理 ALSA 音频输入输出；PL 运行 HLS 融合最小相位变换；Linux 内核驱动提交缓存一致的 DMA 缓冲区。
- 本项目不是 PYNQ 项目。AMD 指南允许自主命题赛道采用 PS 软件与 HLS/RTL 组合；PYNQ 是初学组建议使用的框架，不是强制要求。

## 来源与版本

已部署的 Round30 源码版本为 `Pi-debug-cmd/2026_FPGA` 仓库中的 `a8f6f8f32b159eaea277354118220c633f31fbc2`，任务编号为 `PL-20261027-01`。原开发分支之后加入了独立的合成脉冲实验；这些后续实验不属于本项目包。

## 目录说明

| Path | Contents |
| --- | --- |
| `src/` | HLS 核、PS 运行时/后端、Linux DMA 驱动，以及本次构建使用的 WORLD 上游文件 |
| `build/` | HLS/Vivado Tcl、ARM 构建、质量检查和位流打包脚本 |
| `board/` | 持久化启动、安装、恢复和运行时清单 |
| `sim/` | 确定性 HLS 测试平台和启动故障注入测试 |
| `data/metrics/` | 竞赛格式的指标摘要及校验脚本 |
| `report/` | Round16-30 的设计、实现、板端、实时音频和重启证据 |
| `board/artifacts/round30/` | Release 中 FPGA 输出文件的哈希清单和校验说明 |
| `board/hardware/round30/` | Vivado `.xsa`、硬件交接文件和可移植源码包（Release 附件） |
| `board/` | 板卡配置、部署脚本、运行时清单和 PetaLinux 镜像获取说明 |
| `report/` | 设计报告、架构、接口、复现指南、提交清单和 AI 协作记录 |
| `skill/` | 可复用的 Vivado MCP、GitHub、DMA、板级启动和回归经验 |

目录名和文件名使用英文 ASCII；文档正文使用中文。

## 快速检查

在仓库根目录运行主机侧启动逻辑检查。需要 Python 3.10+，并确保 POSIX `sh` 已加入 `PATH`：

```sh
python -m unittest sim.test_world_minphase_boot -v
sh -n board/world_minphase_autostart.sh board/world_minphase_init.sh board/world_minphase_control.sh
```

已记录的 HLS 测试使用 24 组确定性向量与 WORLD 0.3.5 对比。测试源码为 `sim/tb_world_minphase.cpp`；按[复现说明](report/reproduction.md)提供 WORLD 0.3.5 源码路径，并使用 Vivado/Vitis HLS 2026.1 运行。HLS C/RTL 协同仿真和板端证据是 `report/` 中的历史结果。生成的 FPGA 文件作为 Round30 Release 附件提供，不提交到 Git。

## 复现范围与限制

部分项目输入仍需从外部获取：Vivado/Vitis 2026.1、构建脚本使用的完整 WORLD 0.3.5 源码，以及 PetaLinux 2022.2 板端镜像/工程。完整 Vivado 工程源码包作为 Release 附件提供，但不含运行输出，且未进行干净环境下的全流程布线重建。获取和重建 PetaLinux 的建议路径见[PetaLinux 镜像获取说明](board/petalinux_image_acquisition.md)。在其他板卡上运行安装脚本前，必须先核对记录的出厂文件哈希并审阅部署流程。

原始人声、生成音频、Linux 镜像、模块、可执行文件和 Vivado 缓存均不包含在仓库中。Release 仅包含识别 Round30 实现所需的 FPGA 配置载荷、硬件交接文件和报告。数值 HLS 核的构建和测试不需要音频，核回归使用确定性合成向量。仓库保留已发布的语音测试摘要，但不再分发音频本身。

## AMD 赛道适配情况

本项目面向 AMD FPGA 自主命题赛道（AMD 2026 指南第 3.3 节），使用允许的 Zynq-7000 器件，并采用赛道许可的 PS+HLS 划分。板端演示和干净环境复现要求仍有未完成项；作为正式参赛提交前，请查看提交清单。
