# Reproduction Guide

## Requirements

- Windows host with Vivado/Vitis 2026.1, HLS, and the Zynq-7000 device files; a valid license for the selected implementation steps.
- WORLD 0.3.5 source tree matching the source hash checks in the upstream build scripts.
- A short external build directory to avoid Windows path-length failures.
- For board reproduction: the matching PetaLinux 2022.2 root filesystem, original vendor audio project, and a recoverable Zynq-7020 board setup.

The current package does not include a PetaLinux image. See [PetaLinux image acquisition](petalinux_image_acquisition.md) for recovery from the original build or storage media, and the requirements for a clean rebuild.

The full vendor base project and generated implementation checkpoints were external/ignored source-repository inputs. Therefore the following steps reproduce the individual kernel flow and document how the recorded integrated build was run, but this Git repository alone cannot rebuild the final full-system bitstream from an empty machine.

## HLS kernel simulation and synthesis

From the repository root, set paths to the installed tools and WORLD source. Use a short output root outside deeply nested workspace paths:

```powershell
$worldRoot = 'D:/deps/WORLD-0.3.5'
$env:WORLD_HLS_PROJECT = 'D:/wpl_round30/world_minphase_hls'
& 'D:/Xilinx/Vitis/2026.1/bin/vitis_hls.bat' -f build/cosim_world_minphase_hls.tcl -tclargs $worldRoot
```

Exact executable paths vary by installation. The HLS source/testbench flow performs C simulation, synthesis, and RTL cosimulation. Inspect the reports and exit status; do not infer successful synthesis from a created project directory.

## ARM runtime build

The project's `build/build_world_exp.ps1` has a `-MinphasePl` mode. Supply the matching WORLD source root and an ARM hard-float cross-compiler from the Vivado/Vitis 2026.1 toolchain:

```powershell
./build/build_world_exp.ps1 -WorldRoot 'D:/deps/WORLD-0.3.5' -Target arm -Compiler 'D:/Xilinx/Vitis/2026.1/gnu/aarch32/nt/gcc-arm-linux-gnueabihf/bin/arm-linux-gnueabihf-g++.exe' -MinphasePl
```

Check the script's exact named parameters before running. The generated executable is not tracked.

## Full-system build

The recorded integration used a full vendor audio Vivado project with the generated `world_minphase` IP added to its block design. `build/create_world_exp_20261027.tcl`, `build/add_world_minphase.tcl`, and `build/implement_world_minphase_20261029.tcl` document the project modifications and implementation invocation. Set `WORLD_MINPHASE_IP_REPO` and `WORLD_MINPHASE_PROJECT` to the HLS IP output and full project locations as required by those scripts. The original project checkpoint is not part of this package; reconstructing it requires the source project's vendor base project.

The recorded routed result is in `report/world_minphase_integration_round18_20261029.md`. The system had 13,910 LUT, 20,145 slice registers, 9.5 BRAM tiles, 47 DSP48E1, WNS +0.856 ns, and WHS +0.029 ns. Three input and six output external I/O delays were not constrained, so this was not complete board-I/O timing signoff.

## Test evidence

Host shell injection checks:

```sh
python -m unittest sim.test_world_minphase_boot -v
sh -n board/world_minphase_autostart.sh board/world_minphase_init.sh board/world_minphase_control.sh
```

These tests do not touch a board. Board evidence in `report/` was generated in separate historical trials. Never run an installer or test audio automatically as part of a software build.
