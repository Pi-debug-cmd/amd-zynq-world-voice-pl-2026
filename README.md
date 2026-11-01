# WORLD Minphase PS+PL on Zynq-7020

An AMD FPGA autonomous-topic project package for a real-time WORLD speech pipeline. The programmable logic accelerates the fixed 1024-point WORLD minimum-phase spectral stage. The ARM processing system runs the surrounding WORLD analysis, stream scheduling, and audio I/O.

## Project status

This is a source-and-evidence package for the Round30 implementation. The user accepts Round9's five offline objective metrics as a basic pass, the original Round10 listening as a subjective pass, and the existing Round23/30 board evidence as a pass for the stability and latency acceptance criteria. Round24 had no valid speech and is excluded from that decision. The central technical contribution is PS/PL cooperation: the ARM PS runs the WORLD stream and audio path while the HLS accelerator and DMA interface execute the selected minimum-phase stage in PL. This package does not claim that the whole WORLD pipeline runs in PL. See [the design report](report/DESIGN_REPORT.md) and [the checklist](SUBMISSION_CHECKLIST.md).

The `round30-submission-20261101-v2` GitHub Release contains the matching Round30 board payload, `.bit`, `.hwh`, `.xsa`, a compact Vivado project source archive, and routed implementation reports. The archive was extracted into a clean directory and opened with Vivado 2026.1; its Zynq block design validated. A full synthesis/implementation rebuild is not claimed: generated run results are excluded, while the PetaLinux image remains pending. SHA-256 values and provenance are listed in [the artifact manifest](artifacts/round30/MANIFEST.md).

## Platform and implementation

- Board: Wildfire Zynq-7020, device `xc7z020clg400-2`.
- Toolchain: Vivado/Vitis 2026.1; Linux PetaLinux runtime on the board.
- Software/hardware split: C++ WORLD streaming runtime and ALSA I/O on PS; HLS fused minimum-phase transform on PL; Linux kernel driver submits coherent DMA buffers.
- This is not a PYNQ project. The AMD guide permits PS software and HLS/RTL combinations for the autonomous-topic track. PYNQ is a recommendation for the beginner group, not a mandatory framework.

## Provenance

The deployed Round30 source revision is `a8f6f8f32b159eaea277354118220c633f31fbc2` from `Pi-debug-cmd/2026_FPGA`, task `PL-20261027-01`. The containing development branch later added separate synthesis-pulse experiments; those later experiments are not part of this package.

## Package map

| Path | Contents |
| --- | --- |
| `src/` | HLS core, PS runtime/backend, Linux DMA driver, and the WORLD upstream files used by this build |
| `build/` | HLS/Vivado Tcl, ARM build, quality check, and bitstream packaging scripts |
| `board/` | Persistent boot, install, recovery, and runtime manifests |
| `sim/` | Deterministic HLS testbench and boot failure-injection tests |
| `metrics/` | Competition-style metric summary and test entry points |
| `report/` | Round16-30 design, implementation, board, live-audio, and reboot evidence |
| `artifacts/round30/` | Hash manifest and validation instructions for Release-only FPGA outputs |
| `hardware/round30/` | Vivado `.xsa`, hardware handoff, and portable source-project archive |
| `docs/` | Architecture, interfaces, hardware setup, PetaLinux image acquisition, and AI collaboration record |
| `skill/` | Reusable Vivado MCP, GitHub, DMA, bring-up, and regression notes |

The folder and file names are English-only. Chinese is used only in document contents.

## Quick checks

Run host-side boot logic checks from the repository root with Python 3.10+ and a POSIX `sh` available on `PATH`:

```sh
python -m unittest sim.test_world_minphase_boot -v
sh -n board/world_minphase_autostart.sh board/world_minphase_init.sh board/world_minphase_control.sh
```

The recorded HLS test is a deterministic 24-vector comparison against WORLD 0.3.5. Its source is `sim/tb_world_minphase.cpp`; run it using Vivado/Vitis HLS 2026.1 and the WORLD 0.3.5 source path as described in [reproduction](docs/reproduction.md). The HLS C/RTL cosimulation and board evidence are historical results in `report/`. Generated FPGA outputs are attached to the Round30 Release, not committed to Git.

## Reproduction boundary

Some project inputs are intentionally external: Vivado/Vitis 2026.1, the complete WORLD 0.3.5 source tree used by the build scripts, the vendor audio base project, and the PetaLinux 2022.2 board image. The source repo did not contain the full generated base project or board image. See [PetaLinux image acquisition](docs/petalinux_image_acquisition.md) for the preferred recovery and rebuild paths. The scripts and exact dependencies are documented, but a clean-room full bitstream rebuild was not possible from tracked files alone. Do not run the board installation scripts on another board without first matching the recorded factory hashes and reviewing the deployment procedure.

Raw human speech, generated audio, Linux images, modules, executables, and Vivado caches are excluded. The Release contains only the FPGA programming payload and handoff/report files needed to identify the Round30 implementation. Audio is not needed to build or test the numeric HLS kernel; synthetic deterministic vectors are used for the kernel regression. Published speech-test summaries are retained, but the audio itself is not redistributed.

## AMD track fit

The work is scoped for the AMD autonomous-topic FPGA track (section 3.3 of the 2026 AMD guide). It uses an allowed Zynq-7000 device and a permitted PS+HLS split. The guide's board-demo and clean-reproduction requirements remain open for this package; see the checklist before treating it as a final contest submission.
