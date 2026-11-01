# Hardware Setup

## Recorded platform

- Board: Wildfire Zynq-7020 development board.
- Device: `xc7z020clg400-2`.
- FPGA toolchain: Vivado/Vitis 2026.1.
- Board software: PetaLinux 2022.2, Linux 5.15.0-xilinx.
- Audio codec: WM8960; the tested physical chain used the external microphone input and speaker/headphone output described in the source project's hardware notes.
- Recorded ALSA transport: 32 kHz, S24_LE, two channels; the WORLD algorithm's internal stream is mono 16 kHz.

This is not a PYNQ-Z2 board image or a PYNQ overlay package. It is a Linux/PetaLinux deployment using a custom bitstream, an out-of-tree kernel module, a C++ runtime, and init scripts.

## Safe reproduction boundary

The persistent deployment scripts verify factory hashes and are tied to the exact original image and board state used in 2026-10-30. They are not generic installers. Before adapting them, obtain a recoverable image, verify all baseline files on the target, inspect every absolute path and expected hash, and prepare a rollback plan. The project reports record preservation checks for the original boot files; they do not authorize running these scripts on an arbitrary board.

No fresh board operation, microphone capture, playback, or listening test is performed by packaging this repository. Any new physical audio test needs the operator's readiness confirmation and a newly recorded trial.
