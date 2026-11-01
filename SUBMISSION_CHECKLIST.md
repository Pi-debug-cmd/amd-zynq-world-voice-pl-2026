# Submission Checklist

Reference: *FPGA Innovation Design Competition 2026 Topic Guide (AMD)*, section 3.3, especially 3.3.2-3.3.5. The official guide is not redistributed in this repository.

| Requirement | Package evidence | Status |
| --- | --- | --- |
| Allowed AMD FPGA and declared part | Wildfire Zynq-7020, `xc7z020clg400-2`, in README and hardware setup | Present |
| Complete FPGA work with PS/HLS allowed | HLS minimum-phase core, PS runtime/backend, Linux driver | Present |
| Board execution and measured output | Rounds20, 23, and 30; Round23 has operator-confirmed audible output | Partial; Round30 is a boot/deployment result |
| Reproducible source, build, simulation | Source, Tcl, PowerShell, shell, deterministic testbench | Partial; external vendor base project and tool installs are not included |
| Synthesis/implementation reports and resources | Round17 OOC and Round18 routed system reports | Present; external audio I/O delays are incomplete |
| Performance baseline and gain | Round20 reports CPU/PL wall time and numeric error | Present; measured speed gain is small (2.66%-3.39% for two samples) and not statistically conclusive |
| System/voice application objective | Reports preserve speech trials and target limits | Incomplete; no final voice identity or objective conversion-quality pass |
| Stability and recovery | Round30 reboot recovery; Round24 records an invalid no-speech run | Incomplete; no valid 30-minute speech stability result |
| English-only path and file names | All package paths use English ASCII names | Present |
| Reusable Skill with scope and limits | `skill/` | Present; only project-local clean deployment has been evidenced |
| AI collaboration prompts, answers, and corrections | `docs/ai_collaboration.md` | Partial; this is a task-focused record, not a full export of every historical chat |
| Open-source license | Root MIT license for project-authored content; upstream WORLD license retained | Present; see license scope |
| Final deliverables (`.bit` / `.xsa` / `.hwh`) | Build instructions and generated artifact hashes in source reports | Not included; generated artifacts were absent/ignored in the source repository |
| PYNQ framework | Not used; Linux/PetaLinux C++ PS runtime is used | Not required by the autonomous-topic track; beginner group recommends PYNQ |
| Final-round material | Official guide also requires a one-page English poster using AMD's template for finalist teams | Not included; template/entry status was not available in this project checkout |

The archive is an honest project package and evidence snapshot. It is not yet a fully closed contest submission. Before claiming full completion, rebuild from a clean environment, regenerate and attach allowed FPGA deliverables, complete valid long-duration speech testing, and document the final application-quality gate.
