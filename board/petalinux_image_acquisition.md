# PetaLinux Image Acquisition

## Recorded target

- Board: Wildfire Zynq-7020, `xc7z020clg400-2`.
- Runtime recorded on the board: PetaLinux 2022.2, Linux `5.15.0-xilinx`.
- The submission Release contains the Round30 `.xsa` and FPGA programming artifacts, but not a PetaLinux project or bootable image.

## Preferred path: recover the exact deployed image

Ask the engineer or workstation that created the board image for the original PetaLinux project and its release output. Request the complete project or BSP, configuration files, layers, and the matching image files, not just `image.ub`. Depending on the project configuration, the boot set may include `BOOT.BIN`, `image.ub`, a separate root filesystem, boot configuration, and the SD-card image (`.wic`). Record SHA-256 for every file and confirm the PetaLinux release and kernel version.

If the original build files are unavailable but the original boot medium still exists, make a read-only, full-media image using a verified card reader and a separate destination drive. First identify the medium by its model and capacity. On Linux, a raw read can use `dd` with the verified source device as `if` and a regular file on another drive as `of`; never point `of` at a block device. Do not image a card while it is in use by a powered board. Preserve the original medium and validate the copy before attempting any recovery. If the board boots from QSPI, eMMC, or another device, use the matching recovery process rather than assuming an SD card.

A full-media image is the best route to preserve the exact deployed partitions and configuration. It may contain board-specific settings or credentials, so review and handle it as a controlled artifact before sharing or uploading it.

## Rebuild path

If no image can be recovered, a reproducible rebuild requires all of the following:

- PetaLinux 2022.2 installed in a supported Linux build environment.
- The original PetaLinux project or BSP, including `project-spec`, kernel/rootfs configuration, device-tree customization, and required layers.
- The hardware handoff (`.xsa`) that matches that PetaLinux project and board design.
- The exact bootloader, kernel, rootfs, firmware, and application dependencies used by the deployed runtime.
- Access to the required vendor downloads and licenses.

The `.xsa` in this submission was exported using Vivado 2026.1. Compatibility with the original PetaLinux 2022.2 project has not been verified. Prefer the XSA archived with the original PetaLinux project; otherwise treat a tool-version migration as a separate port and validate it on a recoverable board setup. An XSA alone describes hardware and cannot reconstruct the original kernel, rootfs packages, device tree, or boot policy.

After a successful PetaLinux build, retain the project/BSP and generated boot files together. Package a complete SD image if the project provides one; otherwise document the partition layout and provide every required boot and rootfs artifact. Verify hashes and boot the image from a spare medium before considering it a replacement. Do not overwrite the only known-good board medium during image acquisition.

## Current status

The provided local directory named `Petalinux安装文件` contains only `plnx-env-setup.sh`. That script installs Ubuntu host dependencies; it is not the PetaLinux installer. Ubuntu 20.04 is available through WSL, but no PetaLinux 2022.2 `.run` installer was found in the searched download and project locations. No `.wic`, `.bsp`, PetaLinux project, `BOOT.BIN`, or `image.ub` is included in this repository or the Round30 Release.

The two Wildfire tutorial `rootfs.tar.gz` files in the资料盘 belong to separate Zynq-7020/Zynq-7010 tutorial Linux trees. They are not the recorded PetaLinux 2022.2 system image and must not be substituted for it.

The official AMD PetaLinux page is https://www.amd.com/zh-cn/products/software/adaptive-socs-and-fpgas/embedded-software/petalinux-sdk.html. Its download section links to the embedded-software downloads page and the legacy-version catalog. AMD's published download index currently lists the 2022.2 installer as `petalinux-v2022.2-10141622-installer.run` (2.58 GB; MD5 `8ee3e168ed891b467d248789cea8e484`) behind AMD account/license acceptance: https://account.amd.com/en/forms/downloads/xef.html?filename=petalinux-v2022.2-10141622-installer.run. This is the tool installer, not the project's bootable board image. Download it only from AMD after signing in and accepting the applicable terms.

The next practical action is to obtain the official PetaLinux 2022.2 installer from AMD and locate the original PetaLinux project/BSP and matching XSA. Alternatively, recover a verified read-only image from the original board boot medium. A fresh build cannot proceed from the environment setup script and Round30 `.xsa` alone.
