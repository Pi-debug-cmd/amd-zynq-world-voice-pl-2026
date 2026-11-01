# Round30 Hardware Deliverables

The `round30-submission-20261101-v4` GitHub Release includes `voice7020.xsa`, `voice7020_project_sources.tar.gz`, and `voice7020_project_sources.zip`. The compact tar archive is convenient for source review. The 104 MB full `archive_project` ZIP contains the Vivado `.xpr`, Zynq block design, imported RTL/XDC, custom IP definitions, and generated IP sources/netlists. Its run outputs are excluded.

Both archives were extracted to empty directories and opened in Vivado 2026.1. `open_bd_design` read the Zynq design and `validate_bd_design` passed. This verifies archive portability and block-design integrity; it does not claim a fresh synthesis/implementation run. Run results are omitted because the matching routed reports and programming outputs are separately included.

The XSA was exported from the completed `impl_1` routed checkpoint using `write_hw_platform -fixed -include_bit`. It contains `voice7020.bit`, `zynq.hwh`, PS initialization data, and generated driver stubs. Its embedded bitstream SHA-256 must match the standalone `.bit` in `../../artifacts/round30/MANIFEST.md`.

The board runtime image is PetaLinux 2022.2 and is not included. The exact image/project is pending recovery or rebuild; do not treat the XSA as a Linux image.
