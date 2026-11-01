# Collaboration Log

## SUBMIT-20261101-02 - 2026-11-02 - packaging

- Status: PROPOSED
- Base commit: `92b5ba4` (`round30-submission-20261101-v4`)
- Change: reorganize the submission to the AMD guide's `src/`, `sim/`, `build/`, `board/`, `data/`, `skill/`, and `report/` layout; update links, metric validation paths, and artifact ignore rules.
- Paths: `README.md`, `.gitignore`, `board/`, `data/`, `report/`, `coummucation.md`.
- Reproduction/checks: `python data/metrics/scripts/validate_metrics.py`; `python -m unittest sim.test_world_minphase_boot -v`; `git diff --check`.
- Results: all 23 metric rows resolve to existing evidence; boot logic tests pass where host capabilities permit (two shell-dependent cases skipped on Windows).
- Limits: POSIX shell syntax validation was unavailable on the Windows host; no hardware, audio, Vivado, or PetaLinux test was run for this documentation-only reorganization.
- Next responsibility: repository maintainer to review and merge the updated submission PR.
