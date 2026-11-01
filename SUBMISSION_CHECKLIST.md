# Submission Checklist

Reference: *FPGA Innovation Design Competition 2026 Topic Guide (AMD)*, section 3.3, especially 3.3.2-3.3.5. The official guide is not redistributed in this repository.

| Requirement | Package evidence | Status |
| --- | --- | --- |
| Allowed AMD FPGA and declared part | Wildfire Zynq-7020, `xc7z020clg400-2`, in README and hardware setup | Present |
| Complete FPGA work with PS/HLS allowed | HLS minimum-phase core, PS runtime/backend, Linux driver | Present |
| Board execution and measured output | Round23 valid live speech, timing/runtime telemetry, zero xrun/fallback; Round30 reboot with active PL calls | Pass by user acceptance based on existing Round23/30 board evidence; Round24 is excluded because it had no valid speech |
| Reproducible source, build, simulation | Compact and full Vivado source archives, Tcl, PowerShell, shell, deterministic testbench; both clean extractions open and BD validate in Vivado 2026.1 | Source present; full routed rebuild was not run and PetaLinux image/project is pending |
| Synthesis/implementation reports and resources | Round17 OOC and Round18 routed system reports | Present; external audio I/O delays are incomplete |
| PS/PL cooperation | ARM PS streaming/audio runtime, HLS minphase IP, coherent DMA driver, board-side calls and fallback counter | Implemented and exercised on Zynq-7020 |
| System/voice application objective | Round9 frozen new-session offline five-gate report: identity 0.5200, P10 0.4719, source leakage 0.0591, UTMOS 3.0789, CER 0.1020; original Round10 listening | Basic objective pass and subjective timbre pass by user acceptance |
| Stability and latency acceptance | Round23: 20-second valid speech, analysis max 34.605 ms, zero xrun/ALSA errors/fallback; Round30: rebooted candidate with PL calls increasing from 2,278 to 13,751 | Pass by user acceptance based on existing board evidence; Round24 is excluded because it had no valid speech |
| English-only path and file names | All package paths use English ASCII names | Present |
| Reusable Skill with scope and limits | `skill/`, including a PS/PL prompt sequence | Present; the prompt sequence has not been independently forward-tested |
| AI collaboration prompts, answers, and corrections | `docs/ai_collaboration.md` | Partial; this is a task-focused record, not a full export of every historical chat |
| Open-source license | Root MIT license for project-authored content; upstream WORLD license retained | Present; see license scope |
| Final deliverables (`.bit` / `.xsa` / `.hwh`) | Round30 Release includes `.bit`, `.bin.gz`, `.hwh`, `.xsa`, source-project archive, and routed reports with SHA-256 manifest | Present; PetaLinux image remains pending |
| PYNQ framework | Not used; Linux/PetaLinux C++ PS runtime is used | Not required by the autonomous-topic track; beginner group recommends PYNQ |
| Final-round material | Official guide's one-page English poster applies to finalist teams | Not applicable now; the team has not entered finalist status |

This is an engineering submission snapshot. Both Vivado source archives reopen and validate their block design; the full archive excludes synthesis/implementation run outputs, and the PetaLinux image/project is not included. The user accepts Round9's five objective gates, the original Round10 listening, and stability/latency based on the existing Round23/Round30 evidence. The technical contribution is the PS/PL division of the real-time WORLD path, not a claimed end-to-end speed gain.
