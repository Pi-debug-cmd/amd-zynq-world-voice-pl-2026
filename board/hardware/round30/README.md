# Round30 硬件交付物

GitHub Release `round30-submission-20261101-v4` 包含 `voice7020.xsa`、`voice7020_project_sources.tar.gz` 和 `voice7020_project_sources.zip`。精简 tar 包便于审查源码。104 MB 的完整 `archive_project` ZIP 包含 Vivado `.xpr`、Zynq Block Design、导入的 RTL/XDC、自定义 IP 定义及生成的 IP 源码/网表，不包含运行输出。

两个源码包都曾解压到空目录，并在 Vivado 2026.1 中打开。`open_bd_design` 成功读取 Zynq 设计，`validate_bd_design` 通过。这验证了源码包的可移植性和 Block Design 完整性，但不代表重新执行了综合/实现。由于已单独提供匹配的布线报告和配置文件，因此未附带运行结果目录。

XSA 是从完成布线的 `impl_1` 检查点使用 `write_hw_platform -fixed -include_bit` 导出的，包含 `voice7020.bit`、`zynq.hwh`、PS 初始化数据和生成的驱动桩代码。XSA 内嵌位流的 SHA-256 应与 `../../artifacts/round30/MANIFEST.md` 中单独提供的 `.bit` 哈希一致。

板端运行环境为 PetaLinux 2022.2，但项目包不包含该镜像。确切镜像/工程仍待恢复或重建；XSA 不能作为 Linux 镜像使用。
