# PS/PL Interface

## Hardware contract

| Item | Value |
| --- | --- |
| HLS top | `world_minphase` |
| Target | `xc7z020clg400-2` |
| Input | 513 `float32` log-spectrum bins |
| Output | 513 `float32` real and 513 `float32` imaginary filter bins |
| Transform size | 1024 points |
| Control register window | `0x43C70000` |
| Pointer argument window | `0x43C80000` |
| DDR path | HLS masters through `minphase_mem` to PS `S_AXI_HP2` |
| Clock | PS `FCLK_CLK0`, 100 MHz in recorded integration |
| Completion | HLS control/interrupt; Linux driver uses bounded polling in the recorded path |
| Linux interface | `/dev/world_minphase`, ioctl `WORLD_MINPHASE_PROCESS` |

The authoritative register and packet layouts are in `src/kernel/world_minphase_ioctl.h`, `src/kernel/world_minphase_dma.c`, and `src/ps/world_minphase_pl.cpp`. Do not infer register offsets from this summary when changing the implementation.

## Runtime selection

`WORLD_MINPHASE=cpu` selects the software implementation. `WORLD_MINPHASE=pl` requires `/dev/world_minphase`; open or ioctl failure aborts the process. The implementation tracks call, fallback, copy, device, unpack, and mutex-wait time. A request for a non-1024 FFT size follows the CPU fallback path and increments the fallback counter.

The end-to-end audio runtime additionally expects the source project's WORLD 0.3.5 dependencies, 16 kHz internal mono PCM processing, and the board's existing ALSA/codec configuration. The recorded physical interface was 32 kHz, S24_LE, stereo at ALSA, with explicit conversion in the runtime.
