# PetaLinux 镜像获取说明

## 已记录的目标环境

- 板卡：Wildfire Zynq-7020，`xc7z020clg400-2`。
- 已记录的板端运行环境：PetaLinux 2022.2、Linux `5.15.0-xilinx`。
- 提交包 Release 包含 Round30 `.xsa` 和 FPGA 配置制品，但不包含 PetaLinux 工程或可启动镜像。

## 首选路径：恢复实际部署的镜像

向创建板端镜像的工程师或工作站索取原始 PetaLinux 工程及其发布输出。应索取完整工程或 BSP、配置文件、层和匹配的镜像文件，不能只要 `image.ub`。根据工程配置，启动文件可能包括 `BOOT.BIN`、`image.ub`、独立根文件系统、启动配置以及 SD 卡镜像（`.wic`）。记录每个文件的 SHA-256，并确认 PetaLinux 发布版本和内核版本。

如果原始构建文件已无法取得，但原启动介质仍在，可使用已确认的读卡器，将介质只读完整镜像到另一块独立磁盘。首先通过型号和容量识别介质。在 Linux 中，可使用 `dd` 对已确认的源设备执行原始读取，并将输出 `of` 指向另一磁盘上的普通文件；绝不能把 `of` 指向块设备。板卡通电使用存储卡时不要制作镜像。保留原介质，并在尝试恢复前验证副本。如果板卡从 QSPI、eMMC 或其他介质启动，应使用对应的恢复流程，不要默认其启动介质是 SD 卡。

完整介质镜像最有利于保留实际部署的分区和配置。镜像可能包含板卡专属设置或凭据，因此分享或上传前应将其作为受控制品审查和处理。

## 重建路径

如果无法恢复镜像，要实现可复现重建，至少需要以下材料和条件：

- 在受支持的 Linux 构建环境中安装 PetaLinux 2022.2。
- 原始 PetaLinux 工程或 BSP，包括 `project-spec`、内核/rootfs 配置、设备树定制和所需层。
- 与该 PetaLinux 工程及板卡设计匹配的硬件交接文件（`.xsa`）。
- 已部署运行时使用的准确 Bootloader、内核、rootfs、固件和应用依赖。
- 获取所需厂商下载文件和许可证的权限。

本提交包中的 `.xsa` 使用 Vivado 2026.1 导出，尚未验证其与原始 PetaLinux 2022.2 工程的兼容性。优先使用原 PetaLinux 工程中归档的 XSA；否则应把工具版本迁移作为单独移植任务，并在可恢复的板卡环境中验证。XSA 只描述硬件，不能单独重建原始内核、rootfs 软件包、设备树或启动策略。

PetaLinux 构建成功后，应将工程/BSP 与生成的启动文件一并保存。如果工程能够生成完整 SD 镜像，就提交完整镜像；否则应说明分区布局并提供所有必需的启动文件和 rootfs 制品。核对哈希，并先从备用介质启动验证，再考虑将其作为替代镜像。获取镜像期间不要覆盖唯一已知可用的板卡介质。

## 当前状态

提供的本地目录 `Petalinux安装文件` 中只有 `plnx-env-setup.sh`。该脚本用于安装 Ubuntu 主机依赖，并非 PetaLinux 安装程序。WSL 中可使用 Ubuntu 20.04，但在已检查的下载目录和工程目录中没有找到 PetaLinux 2022.2 `.run` 安装包。本仓库和 Round30 Release 均不包含 `.wic`、`.bsp`、PetaLinux 工程、`BOOT.BIN` 或 `image.ub`。

资料盘中的两个 Wildfire 教程 `rootfs.tar.gz` 分别属于 Zynq-7020/Zynq-7010 教程 Linux 工程，不是已记录的 PetaLinux 2022.2 系统镜像，不能替代该镜像。

AMD 官方 PetaLinux 页面为：https://www.amd.com/zh-cn/products/software/adaptive-socs-and-fpgas/embedded-software/petalinux-sdk.html。其下载区域链接到嵌入式软件下载页面和旧版本目录。AMD 已发布的下载索引列出了 2022.2 安装程序 `petalinux-v2022.2-10141622-installer.run`（2.58 GB；MD5 `8ee3e168ed891b467d248789cea8e484`），需登录 AMD 账户并接受许可条款后获取：https://account.amd.com/en/forms/downloads/xef.html?filename=petalinux-v2022.2-10141622-installer.run。此文件是工具安装程序，不是本项目可启动的板卡镜像。请登录 AMD 并接受适用条款后再下载。

下一步应从 AMD 获取官方 PetaLinux 2022.2 安装程序，并找到原始 PetaLinux 工程/BSP 及匹配的 XSA。另一种方式是从原板卡启动介质恢复并验证只读镜像。仅凭环境设置脚本和 Round30 `.xsa` 无法完成全新构建。
