# Round30 FPGA 制品清单

Release 标签：`round30-submission-20261101-v4`
源项目：`Pi-debug-cmd/2026_FPGA`，已部署源码版本 `a8f6f8f32b159eaea277354118220c633f31fbc2`，任务 `PL-20261027-01`。
实现证据：[Round18 集成报告](../../../report/world_minphase_integration_round18_20261029.md)和[Round30 持久启动报告](../../../report/world_minphase_persistent_boot_round30_20261030.md)。

归档中包含以下文件：

| 文件 | 字节数 | SHA-256 | 用途 |
| --- | ---: | --- | --- |
| `world_minphase_swap.bin.gz` | 536768 | `6a7fec9987d31c5f803b79b1bb8e115dca9fda0dfc278b8f462d60562b628d98` | 字节序已交换的 FPGA Manager 启动载荷；与 Round30 已部署候选版本哈希一致 |
| `zynq_wrapper.bit` | 4045767 | `e2131f0c4306f891e05f9a5aa9cee33077ad794b3ab2a2a53e0eac9d67b8cee3` | Vivado 2026.1 布线位流 |
| `zynq.hwh` | 667289 | `d510e66789afa9b08fbb27474ce91e01bf231485c08dc03d68db875c3b2fa7ff` | Block Design 硬件交接元数据 |
| `timing_summary.txt` | 56255 | `db35e15e23fb0d8e233a0c7ed7b0ea33775e261d65a4cd1de857144271a29471` | 布线时序报告 |
| `utilization.txt` | 13464 | `604f4c0671e9d8fd4915b51820807f7493a4edfcf5001ddc2ccc42d6d7cc1282` | 实现资源报告 |
| `drc.txt` | 150347 | `6b65a4b0b80d45657bb7d6db9b2ac39be67310f6beb22a5901d8b0e98ba37bae` | DRC 报告 |
| `route_status.txt` | 651 | `ea5fbbf95224e790ebffe022e5a1c082abbf847d4f04dbd106d707ea0d801403` | 布线完成状态摘要 |
| `bus_skew.txt` | 75314 | `4179efc918c1699096d6f84a3cf381ded90f66d16cde1da75355ba35d14cc8c4` | 布线后的总线偏斜报告 |
| `world_minphase_bit_manifest.json` | 569 | `8aa5ef115d09acb5c693bd6817a1ebe477b7894baf6ef0511c5c742a659f714e` | 载荷元数据及原始/交换后哈希的机器可读清单 |
| `voice7020.xsa` | 958768 | `fc69ad520846b27dcdc1620778f28371f7ef477c521a56d9d40c12dbefbba3cc` | 内嵌位流的导出硬件平台文件 |
| `voice7020_project_sources.tar.gz` | 626213 | `12d723cd4cd9e384d196ea105a4a6be200aee50ebb12398ad71e6d7cf869fd5f` | 精简 Vivado 工程源码包；不含生成网表和运行结果 |
| `voice7020_project_sources.zip` | 104087259 | `37f22a2e37af3290c1826a5257a5148771a8a6307da1355e5f4f32c2772d851d` | 完整 Vivado `archive_project` 源码包；含生成的 IP，不含运行输出 |

载荷、`.bit` 和报告的哈希记录在 Round18/Round30 证据中。`.hwh` 和 JSON 清单哈希根据保留的 Vivado 导出文件及打包清单计算。已核实 XSA 内嵌的 `voice7020.bit` 与独立 `.bit` 文件的 SHA-256 相同。Release 归档本身是实际传输单元。

## 校验方法

从 `https://github.com/Pi-debug-cmd/amd-zynq-world-voice-pl-2026/releases/tag/round30-submission-20261101-v4` 下载 Release 附件，将其解压到对应的 `board/artifacts/round30/` 和 `board/hardware/round30/` 路径，然后运行：

```powershell
Get-FileHash -Algorithm SHA256 .\board\artifacts\round30\world_minphase_swap.bin.gz
Get-FileHash -Algorithm SHA256 .\board\artifacts\round30\zynq_wrapper.bit
Get-FileHash -Algorithm SHA256 .\board\artifacts\round30\zynq.hwh
Get-FileHash -Algorithm SHA256 .\board\hardware\round30\voice7020.xsa
Get-FileHash -Algorithm SHA256 .\board\hardware\round30\voice7020_project_sources.tar.gz
Get-FileHash -Algorithm SHA256 .\board\hardware\round30\voice7020_project_sources.zip
```

将结果与上表进行比较。`.bit` 和 `.hwh` 是该候选版本使用的 Round18 整机实现文件。Round30 修改了持久化部署/启动行为，并复用了相同硬件镜像；已部署压缩载荷的哈希可确认二者相同。

## 限制

精简源码包包含 Zynq Block Design、工程配置、导入的 RTL/XDC、Digilent 音频时钟 IP 和打包的 HLS 核。解压后的工程可在 Vivado 2026.1 中打开，且通过 Block Design 验证。生成的 IP 网表和运行产物按计划排除；尚未从头完成整机布线重建。项目包不含 PetaLinux 镜像、Linux 内核模块和运行时可执行文件。布线时序约束中仍缺少外部音频 I/O 延迟。作为正式竞赛验收前，请先检查提交清单。
