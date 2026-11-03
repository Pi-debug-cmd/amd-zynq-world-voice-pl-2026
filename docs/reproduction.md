# 复现说明

本文按 Round30 板上版本列出从源码检查、HLS 验证、Vivado 工程生成到 ARM 程序和驱动构建的顺序。构建命令只生成文件，不会自动配置或写入板卡；安装脚本仅供确认硬件身份、备份基线和回滚条件后手动执行。

## 环境与外部依赖

- Windows 开发机，Vivado/Vitis HLS 2026.1，并安装 Zynq-7000 器件库。
- Linux/PetaLinux 板端；本项目使用野火 PetaLinux 2022.2 与 WM8960 音频链路。PetaLinux SDK 从 [AMD 官方入口](https://www.amd.com/zh-cn/products/software/adaptive-socs-and-fpgas/embedded-software/petalinux-sdk.html) 获取；其下载需按 AMD 当前账号和授权条件办理。
- WORLD 0.3.5 上游源码，获取地址：[mmorise/World](https://github.com/mmorise/World)。构建脚本核对 `src/common.cpp` SHA-256 为 `ef4a982d103bfd4c0efe6f1e6fa1192809e07ac39289f29951f3d95f1af8ca51`。
- PetaLinux 对应内核源码/构建目录，用于编译 `world_minphase_dma` 驱动。
- Wildfire Zynq-7020 板卡，器件 `xc7z020clg400-2`，WM8960 音频编解码器。

Vivado 项目输入包括仓库中的 `board/vendor_inputs/`、`board/vendor_project/wildfire_zynq7020_audio_base.zip`、`src/rtl/` 和 Tcl 脚本。供应商基础工程 ZIP 保持原样；其 SHA-256 和内容边界见 `board/vendor_project/MANIFEST.md`。生成的 `.bit`、`.bin`、HLS 工程、ARM 可执行文件、驱动模块和 PetaLinux 镜像由复现环境生成或按厂商渠道获取，不放入源码归档。

## 获取代码并核对版本

```sh
git clone https://github.com/Pi-debug-cmd/amd-zynq-world-voice-pl-2026.git
cd amd-zynq-world-voice-pl-2026
git checkout agent/Pi-debug-cmd/SUBMIT-20261103-01
git rev-parse HEAD
```

提交源码的原始实现基线为 `Pi-debug-cmd/2026_FPGA` 中的 `a8f6f8f32b159eaea277354118220c633f31fbc2`。归档提交应与仓库 README 记录的 Round30 基线一致。

## HLS 最小相位核

先选一个短构建路径，避免 Windows 长路径限制，并设置 WORLD 源码目录：

```powershell
$worldRoot = 'D:/deps/World-0.3.5'
$env:WORLD_HLS_PROJECT = 'D:/wpl_round30/world_minphase_hls'
```

创建 HLS 工程并综合：

```powershell
& 'D:/Xilinx/Vitis/2026.1/bin/vitis_hls.bat' `
  -f build/probe_world_minphase_hls.tcl
```

在同一个 `WORLD_HLS_PROJECT` 上运行 C 仿真和 RTL 协同仿真：

```powershell
& 'D:/Xilinx/Vitis/2026.1/bin/vitis_hls.bat' `
  -f build/cosim_world_minphase_hls.tcl -tclargs $worldRoot
```

导出 Vivado IP Catalog IP：

```powershell
& 'D:/Xilinx/Vitis/2026.1/bin/vitis-run.bat' `
  --mode hls --tcl --input_file build/impl_world_minphase_hls.tcl
```

检查综合、C 仿真和 RTL 协同仿真的退出码及报告。`sim/tb_world_minphase.cpp` 以 WORLD 软件实现为黄金参考，覆盖 24 组固定输入；报告中的历史结果不能替代复现者的新运行记录。

## Vivado 整机工程

把 HLS 导出目录和整机工程放到短路径：

```powershell
$env:WORLD_MINPHASE_IP_REPO = 'D:/wpl_round30/world_minphase_hls/solution/impl/ip'
$env:WORLD_MINPHASE_PROJECT = 'D:/wpl_round30/full_system'
& 'D:/Xilinx/Vivado/2026.1/bin/vivado.bat' `
  -mode batch -source build/create_world_exp_20261027.tcl -tclargs minphase
& 'D:/Xilinx/Vivado/2026.1/bin/vivado.bat' `
  -mode batch -source build/implement_world_minphase_20261029.tcl
```

Round30 版本的整机 Tcl 入口沿用提交中的 `create_world_exp_20261027.tcl` 文件名，但已限制为 `minphase` 模式；它为 `xc7z020clg400-2` 建立音频 Block Design，并把 HLS 核的 AXI-Lite 控制和 HP2 DDR 数据接口接入系统。运行前确认环境变量路径正确且输出工程目录为空；实现结束后保存资源、时序、DRC 和路由报告。生成硬件平台时在已生成的 Vivado 工程中导出当前平台并包含 bitstream，记录导出文件 SHA-256。

## ARM 程序和 Linux 驱动

使用 Vitis 2026.1 工具链附带的 ARM hard-float 交叉编译器和 WORLD 源码：

```powershell
./build/build_world_minphase.ps1 `
  -WorldRoot $worldRoot `
  -Target arm `
  -Compiler 'D:/Xilinx/Vitis/2026.1/gnu/aarch32/nt/gcc-arm-linux-gnueabihf/bin/arm-linux-gnueabihf-g++.exe' `
  -MinphasePl
```

若仅构建 CPU 软件参考，省略 `-MinphasePl`。板端 PL 模式通过 `WORLD_MINPHASE=pl` 选择 `/dev/world_minphase`；CPU 模式使用 WORLD 软件实现。构建脚本另生成 24 组板端 DMA 数值探针。

驱动构建需要与板端运行内核完全匹配的源码和输出目录：

```sh
sh build/build_world_minphase_driver.sh \
  /path/to/petalinux/kernel/source \
  /path/to/matching/kernel/build
```

模块与运行文件需在板端按 `board/` 内安装脚本、manifest 和恢复说明部署。脚本不会自动写启动分区；复现前核对板卡、工厂文件 SHA-256 和恢复方法。

## 软件回归与指标检查

```sh
python -m unittest sim.test_world_minphase_boot -v
python metrics/scripts/validate_metrics.py
sh -n board/world_minphase_autostart.sh board/world_minphase_init.sh board/world_minphase_control.sh
```

`metrics/metrics.csv` 中每项数据都链接到 `report/` 的测试条件和结果。Round20 数值核板测、Round23 有效实时语音和 Round30 重启持久启动属于不同验证范围。Round9/10 音色验收及项目长时稳定性、延迟通过结论按项目负责人最终确认记录列示；Round30 的单次重启日志只证明持久启动与该次运行状态，不单独用来推导长时稳定性或未记录的延迟分位数。

## 板端复现

目标系统为野火 PetaLinux 2022.2。获取系统工程或镜像后，先在目标板核实器件、内核、设备树、声卡、现有启动文件和工厂 SHA-256。按 `board/world_minphase_runtime_manifest.json` 准备程序和模块，再根据 `board/install_world_minphase_persistent.sh` 与恢复脚本完成部署。Round23 需要有效语音输入；Round30 需要一次正常重启。录音、播放或试听前必须由现场操作者确认准备状态。

项目技术报告和 Round20/23/30 原始摘要分别记录执行环境、数据范围、输出和校验值。新复现结果须以新的时间戳、源码 SHA 和工具版本保存，不覆盖历史证据。
