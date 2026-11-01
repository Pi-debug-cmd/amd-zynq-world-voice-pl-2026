# Round30 Hardware Deliverables

`voice7020.xsa` and `voice7020_project_sources.zip` are attached to the `round30-submission-20261101-v2` GitHub Release. The source archive was produced by Vivado 2026.1 `archive_project -exclude_run_results -include_config_settings` from the deployed Round18 project. It contains the Zynq block design, project configuration, imported HLS/RTL and vendor audio IP sources, constraints, and local IP repositories.

The archive was extracted to an empty directory and opened in Vivado 2026.1. `open_bd_design` read the Zynq design and `validate_bd_design` passed. This verifies archive portability and block-design integrity; it does not claim a fresh synthesis/implementation run. Run results are omitted because the matching routed reports and programming outputs are separately included.

The XSA was exported from the completed `impl_1` routed checkpoint using `write_hw_platform -fixed -include_bit`. It contains `voice7020.bit`, `zynq.hwh`, PS initialization data, and generated driver stubs. Its embedded bitstream SHA-256 must match the standalone `.bit` in `artifacts/round30/MANIFEST.md`.

The board runtime image is PetaLinux 2022.2 and is not included. The exact image/project is pending recovery or rebuild; do not treat the XSA as a Linux image.
