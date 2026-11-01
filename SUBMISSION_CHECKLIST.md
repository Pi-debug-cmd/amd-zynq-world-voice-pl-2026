# Submission Checklist

Reference: *FPGA Innovation Design Competition 2026 Topic Guide (AMD)*, section 3.3, especially 3.3.2-3.3.5. The official guide is not redistributed in this repository.

| Requirement | Package evidence | Status |
| --- | --- | --- |
| Allowed AMD FPGA and declared part | Wildfire Zynq-7020, `xc7z020clg400-2`, in README and hardware setup | Present |
| Complete FPGA work with PS/HLS allowed | HLS minimum-phase core, PS runtime/backend, Linux driver | Present |
| Board execution and measured output | Rounds20, 23, and 30; Round23 has operator-confirmed audible output | Pass for bounded live run and persistent startup; 30-minute duration is not established |
| Reproducible source, build, simulation | Vivado source archive, Tcl, PowerShell, shell, deterministic testbench; clean extraction opens and BD validates in Vivado 2026.1 | Partial; no from-scratch routed build was run, PetaLinux image pending |
| Synthesis/implementation reports and resources | Round17 OOC and Round18 routed system reports | Present; external audio I/O delays are incomplete |
| Performance baseline and gain | Round20 reports CPU/PL wall time and numeric error | Present; measured speed gain is small (2.66%-3.39% for two samples) and not statistically conclusive |
| System/voice application objective | Round9 frozen new-session offline five-gate report: identity 0.5200, P10 0.4719, source leakage 0.0591, UTMOS 3.0789, CER 0.1020 | Basic pass by user acceptance; Round10 listening report records obvious male residue, so perceived target timbre is not accepted |
| Stability and recovery | Round23 valid 20-second speech trial, Round24 invalid 60-second no-voice trial, Round30 persistent reboot/startup with active PL calls | Pass at the user's accepted scope: bounded live operation plus persistent startup; Round24 is excluded as a valid speech test and 30-minute duration is not established |
| English-only path and file names | All package paths use English ASCII names | Present |
| Reusable Skill with scope and limits | `skill/`, including a PS/PL prompt sequence | Present; the prompt sequence has not been independently forward-tested |
| AI collaboration prompts, answers, and corrections | `docs/ai_collaboration.md` | Partial; this is a task-focused record, not a full export of every historical chat |
| Open-source license | Root MIT license for project-authored content; upstream WORLD license retained | Present; see license scope |
| Final deliverables (`.bit` / `.xsa` / `.hwh`) | Round30 Release includes `.bit`, `.bin.gz`, `.hwh`, `.xsa`, source-project archive, and routed reports with SHA-256 manifest | Present; PetaLinux image remains pending |
| PYNQ framework | Not used; Linux/PetaLinux C++ PS runtime is used | Not required by the autonomous-topic track; beginner group recommends PYNQ |
| Final-round material | Official guide also requires a one-page English poster using AMD's template for finalist teams | Not included; template/entry status was not available in this project checkout |

The package is an engineering submission snapshot, not a claim that every competition gate is closed. Vivado reopened the extracted source archive and validated its block design, but the routed design was not rebuilt from scratch; PetaLinux is pending. The user accepts Round9's five objective gates as a basic pass and the combined Round23/Round30 evidence as stability pass at the stated scope. The Round10 human listening rejection remains visible and limits the target-timbre claim. The finalist poster remains conditional on finalist status and availability of the official AMD template.
