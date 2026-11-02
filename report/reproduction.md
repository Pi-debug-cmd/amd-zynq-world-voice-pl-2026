# 复现指南

## 环境要求

- 安装 Vivado/Vitis 2026.1、HLS 和 Zynq-7000 器件文件的 Windows 主机；所选实现步骤所需的有效许可证。
- WORLD 0.3.5 源码树，且须通过上游构建脚本中的源码哈希检查。
- 较短的外部构建目录，以避免 Windows 路径过长导致失败。
- 板端复现还需要匹配的 PetaLinux 2022.2 根文件系统、原始厂商音频工程，以及可恢复的 Zynq-7020 板卡环境。

当前项目包不包含 PetaLinux 镜像。如何从原始构建或存储介质中恢复，以及干净重建所需的条件，见[PetaLinux 镜像获取说明](../board/petalinux_image_acquisition.md)。

Release 现已包含完整 Vivado `archive_project` 源码 ZIP，其中包括厂商音频设计源码、自定义 RTL/XDC、IP 元数据和生成的 IP 源码。综合/实现运行输出未包含在内。因此，以下步骤可复现独立计算核流程并说明整机集成构建方式，但尚未证明能在全新环境中重新完成整机布线构建。

## HLS 核仿真与综合

在仓库根目录设置工具和 WORLD 源码路径。将输出放在较短的外部目录中，避免工作区目录层级过深：

```powershell
$worldRoot = 'D:/deps/WORLD-0.3.5'
$env:WORLD_HLS_PROJECT = 'D:/wpl_round30/world_minphase_hls'
& 'D:/Xilinx/Vitis/2026.1/bin/vitis_hls.bat' -f build/cosim_world_minphase_hls.tcl -tclargs $worldRoot
```

可执行文件的实际路径因安装位置而异。HLS 源码/测试平台流程会执行 C 仿真、综合和 RTL 协同仿真。请检查报告和退出状态；不能仅凭生成了工程目录就认定综合成功。

## ARM 运行时构建

项目脚本 `build/build_world_exp.ps1` 支持 `-MinphasePl` 模式。提供匹配的 WORLD 源码根目录，以及 Vivado/Vitis 2026.1 工具链中的 ARM 硬浮点交叉编译器：

```powershell
./build/build_world_exp.ps1 -WorldRoot 'D:/deps/WORLD-0.3.5' -Target arm -Compiler 'D:/Xilinx/Vitis/2026.1/gnu/aarch32/nt/gcc-arm-linux-gnueabihf/bin/arm-linux-gnueabihf-g++.exe' -MinphasePl
```

运行前请核对脚本实际支持的命名参数。生成的可执行文件不纳入版本控制。

## 整机工程构建

记录中的集成基于完整的厂商音频 Vivado 工程，并将生成的 `world_minphase` IP 加入 Block Design。`build/create_world_exp_20261027.tcl`、`build/add_world_minphase.tcl` 和 `build/implement_world_minphase_20261029.tcl` 记录了工程修改和实现调用方式。按脚本要求，将 `WORLD_MINPHASE_IP_REPO` 和 `WORLD_MINPHASE_PROJECT` 分别设置为 HLS IP 输出目录和完整工程目录。本项目包不含原始工程检查点；重建整机工程还需要源项目的厂商基础工程。

已记录的布线结果见 `report/world_minphase_integration_round18_20261029.md`。系统资源为 13,910 LUT、20,145 个 Slice 寄存器、9.5 个 BRAM tile、47 个 DSP48E1；WNS 为 +0.856 ns，WHS 为 +0.029 ns。仍有 3 条输入和 6 条输出外部 I/O 延迟未约束，因此这不是完整的板级 I/O 时序签核。

## 测试证据

主机侧 Shell 注入检查：

```sh
python -m unittest sim.test_world_minphase_boot -v
sh -n board/world_minphase_autostart.sh board/world_minphase_init.sh board/world_minphase_control.sh
```

这些测试不会操作板卡。`report/` 中的板端证据来自单独开展的历史测试。软件构建过程中不得自动运行安装程序或测试音频。
