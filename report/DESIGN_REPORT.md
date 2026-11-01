# WORLD Minphase PS+PL Design Report

## 1. Summary

This project integrates a fused 1024-point minimum-phase spectrum kernel into a real-time WORLD speech-processing pipeline on a Wildfire Zynq-7020. The ARM Cortex-A9 PS runs the WORLD stream, analysis/synthesis outside the selected stage, process supervision, and ALSA I/O. A custom HLS accelerator in PL computes the minimum-phase spectrum through a coherent DMA driver.

The project demonstrates PS/PL integration, a numerically matched HLS kernel, routed Zynq integration, board-side DMA execution, live audio, and persistent boot selection. The user accepts the existing Round23 live-audio timing/error evidence together with Round30 persistent-startup evidence as passing the project's stability and latency criteria. This acceptance uses the documented trials and does not imply a new board test.

## 2. Motivation and contribution

WORLD's minimum-phase stage constructs a complex synthesis filter from a log spectral envelope. Its FFT/cepstrum/exp path is a clear hardware boundary: fixed transform size, bounded input/output, deterministic numerical comparison, and a measurable call counter. The implementation fuses transform and nonlinear operations in one HLS IP and connects it to PS DDR through HP2, rather than treating the FPGA as an I/O adapter.

The engineering contribution is the end-to-end integration and recovery behavior around that accelerator: PS hook selection, a Linux coherent-DMA interface, bounded driver behavior, audio runtime telemetry, verified candidate installation, and boot fallback/guard controls. This work is an implementation contribution; it does not claim a new speech-conversion model.

## 3. Architecture and interface

The data path and interface are described in [architecture](architecture.md) and [interface](interface.md). The HLS function consumes 513 float32 log-spectrum bins and produces 513 complex float32 filter bins for a 1024-point transform. Two AXI-Lite control windows are assigned at `0x43C70000` and `0x43C80000`. HLS input and output masters use a dedicated interconnect to PS HP2 DDR. The recorded clock is 100 MHz from `FCLK_CLK0`.

## 4. Design and validation history

| Stage | Evidence | Result and limit |
| --- | --- | --- |
| HLS cosimulation | [Round16](world_minphase_cosim_round16_20261029.md) | RTL cosim for deterministic 24-case testbench; see report for numerical threshold |
| HLS OOC implementation | [Round17](world_minphase_ooc_round17_20261029.md) | Kernel-level implementation only, not full-system signoff |
| Full design integration | [Round18](world_minphase_integration_round18_20261029.md) | Routed system: 13,910 LUT, 20,145 registers, 9.5 BRAM tiles, 47 DSP; WNS +0.856 ns, WHS +0.029 ns. External I/O delays remain incomplete |
| Board numeric path | [Round20](world_minphase_board_round20_20261029.md) | 24/24 vectors; worst relative-L2 `8.53141669193e-7`; two 5-second controlled files at 97.371/96.942 dB SNR, max one PCM16 count, zero fallback/timeout |
| Live audio rejection | [Round21](world_minphase_live20_round21_20261029.md) | Digital pipeline advanced but user reported no audible sound; rejected as a live-audio pass |
| Live audio and latency evidence | [Round23](world_minphase_prompt_live_round23_20261029.md) | 20 seconds, 1,079 voiced frames, analysis max 34.605 ms, zero xrun/ALSA errors, 4,857 PL calls, zero fallback; user said converted audio was audible and similar to PS |
| Excluded speech trial | [Round24](world_minphase_prompt_live60_round24_20261029.md) | 60 seconds with zero voiced frames; excluded from the accepted stability decision because there was no valid speech |
| Persistent deployment and stability evidence | [Round30](world_minphase_persistent_boot_round30_20261030.md) | Normal reboot selected candidate, `READY_CANDIDATE`, capture/playback RUNNING, calls increased from 2,278 to 13,751; accepted together with Round23 evidence |

Round29 and Round30 document the boot race and its correction. Round30 stopped the boot-time test audio service, used process-specific cleanup, cleared stale state before launch, and atomically updated state. It retained original boot asset hashes in the recorded deployment.

## 5. PS/PL cooperation

The PS owns the surrounding WORLD stream, analysis/synthesis outside the selected stage, audio scheduling, ALSA I/O, and runtime supervision. The PL executes the fused 1024-point minimum-phase spectrum stage through an HLS IP. A Linux coherent-DMA driver carries input/output buffers between PS memory and the accelerator; telemetry records calls and fallback behavior. The implementation is presented as a concrete PS/PL partition and integration, without an end-to-end speed-gain claim.

The routed resource and timing figures establish the reported implementation under the tracked project constraints. The report lists three input and six output external I/O delays as missing; therefore its timing result is not complete external interface signoff.

## 6. Application-quality and acceptance limits

The Round9 frozen new-session offline candidate passed the five objective gates: identity 0.5200, P10 0.4719, source leakage 0.0591, UTMOS 3.0789, and CER 0.1020. The user accepts this as a basic pass for the fixed-male offline objective and accepts the original Round10 listening as a subjective pass. The contemporaneous listening note remains in the report as qualitative evidence. This does not establish a PL-deployed conversion-quality pass, multiple unseen speakers, or on-board registration of a new target.

Round21 and Round24 are retained as historical trial records; Round24 is excluded because it contained no valid speech. The user's accepted stability and latency decision is based on the Round23 live run and Round30 persistent-startup evidence. This does not establish unfamiliar-speaker generalization, a PL-deployed conversion-quality pass, or on-board registration of a new target.

## 7. Reproduction and release content

The repository contains authored HLS, PS, driver, deployment scripts, testbench, skill, and small reports. The HLS test vectors are generated deterministically and require no audio files. Human speech is excluded because it is not necessary for build or numeric tests and is controlled material. Consequently, published speech summary metrics can be inspected but cannot be recreated from the public repository alone.

Full reproduction limits and exact commands are in [reproduction](reproduction.md). The external WORLD 0.3.5 tree, Vivado/Vitis installation, and PetaLinux image remain external. Compact and full Vivado source archives plus the `.xsa` are included in the Round30 Release; both extracted archives open and validate their block design, but a clean-room routed rebuild has not been run. The PetaLinux acquisition options are documented [here](../board/petalinux_image_acquisition.md); the image, `.ko`, and runtime executable remain absent.

## 8. AMD autonomous-topic alignment

Section 3.3 permits HLS, RTL, PS software, and their combination, and requires a board-run work with measured output. Zynq-7000 is permitted. The implementation method is eligible for that track; it does not use PYNQ. PYNQ is a recommendation for the beginner group rather than a universal requirement. The requirement-by-requirement status is in [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md).
