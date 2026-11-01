# Reusable Skills

This directory records workflows derived from the Zynq PS+PL development. The notes can help another team bring up a Linux-based Zynq design, check DMA data movement, compare accelerator output with a golden model, and use Vivado MCP with disciplined Git/GitHub reviews. They are not tied to speech conversion, though board-specific commands still need adaptation.

| Skill | Use | Procedure | Failure conditions | Evidence/source |
| --- | --- | --- | --- | --- |
| `01_board_bringup/` | Establish FPGA/PS state before testing | Check tool version/device, board state, factory hashes, service and PCM status | Wrong image, unverified board state, stale service or missing rollback path | Round30 deployment and recovery reports |
| `02_dma_coherency/` | Integrate AXI DMA-backed accelerator buffers | Keep PS/PL address, alignment, coherency, ownership, timeout, and recovery contracts explicit | Stale cache, unaligned buffer, unbounded wait, mismatched register/packet contract | `src/kernel/world_minphase_dma.c`, Round20 numeric comparison |
| `03_golden_compare/` | Verify HLS/PL outputs against trusted software | Freeze input vectors, compare error metrics and call/fallback counters, keep one variable per round | Unfrozen input, wrong transform scale, fallback hidden as PL success, or test scope overclaimed | Round16, Round20; failures documented in `references/round_lessons.md` |
| `04_vivado_mcp_git_github/` | Run Vivado through MCP and publish traceable task work | Verify Vivado version/part/session, use checked-in Tcl, inspect reports, claim a task, commit/push a scoped change and PR | Wrong installation/device registry, shared session ownership unclear, long MCP command hangs, policy-invalid commit, or evidence stronger than the test | This project has used the tool/debug and collaboration workflow; cross-board reuse is not yet measured |

The steps in these notes were exercised on the project machine and board workflow. They have not been validated by an independent team or on a second board. For another Zynq family, Linux image, tool version, or framework such as PYNQ, treat board paths, driver APIs, clocks, registers, and timing as unverified until independently checked.
