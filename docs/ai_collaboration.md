# AI Collaboration Record

This task-focused record is included for the AMD autonomous-topic requirement to document model-assisted engineering and corrections. It summarizes the packaging conversation and source evidence rather than reproducing unrelated private project chat.

## Work item

- Date: 2026-11-01.
- Source project: `Pi-debug-cmd/2026_FPGA`, branch `agent/Pi-debug-cmd/PL-20261027-01`.
- Round30 implementation revision: `a8f6f8f32b159eaea277354118220c633f31fbc2`.
- Later branch head inspected for provenance only: `6f0d68ba367c920afbef2aa7f7265a5d0176edd3`.
- User direction: make the 2026-10-30 Round30 PS+PL solution a complete submission project, create a corresponding GitHub project, and include audio only if it is necessary.

## Prompts and decisions

1. User asked to package the 2026-10-30 Round30 PS+PL work, not the earlier generic PS+PL experiment.
   - Assistant decision: pin the exact source branch and commit, then read the Round30 report before selecting files.
   - Correction applied: the source PR is still open, so the package records its source SHA and keeps this work in an independent repository.
2. User requested a full submission directory and permitted audio if necessary.
   - Assistant decision: check compilation/test dependencies and distribution constraints before including assets.
   - Correction applied: raw human audio is not required by the HLS build or deterministic synthetic vectors; it is excluded and the report states this limits reproduction of listening tests.
3. User had clarified earlier that the project under discussion is the PS+PL implementation and asked about PYNQ conversion.
   - Assistant decision: classify it against the official AMD autonomous-topic track text.
   - Correction applied: the project is Linux/PetaLinux C++ PS plus HLS PL, not PYNQ; section 3.3 allows PS software with HLS/RTL, while PYNQ is only recommended for the beginner group.
4. User emphasized that this should be treated as a complete project submission.
   - Assistant decision: create the README, architecture/interface/setup/reproduction docs, design report, metrics table, skill, source, scripts, tests, and key evidence.
   - Correction applied: “complete project package” is not equated with “all acceptance gates passed.” Round30 only proves persistent deployment and reboot startup. Long speech stability, final voice quality, full clean-room system rebuild, and generated FPGA deliverables remain explicit gaps.
5. User asked: “提示词流有吗” (Does a prompt flow exist?).
   - Assistant checked the published skill directory and found collaboration notes and hardware/debug skills, but no explicit prompt sequence.
   - Correction applied: added `skill/05_ps_pl_prompt_flow/` with reusable stage prompts for requirements/partitioning, implementation, regression, physical testing, and evidence-based failure review. This is a newly organized workflow; it has not been independently validated by another team.
6. User clarified that the original Round10 listening also passes.
   - Correction applied: the Round10 report now records `ACCEPTED` as the controlling user decision. Its contemporaneous rejection wording remains only as historical context and no longer controls the submission verdict.
7. User confirmed that the existing Round23/30 evidence is accepted for stability and latency, asked that performance gain not be presented, and clarified that the team is not a finalist.
   - Correction applied: the submission summary records stability/latency as accepted from the existing valid live-audio and persistent-startup evidence, presents PS/PL cooperation as the technical contribution, removes speed-gain claims from the summary metrics, and marks finalist material not applicable at this stage.
   - PetaLinux decision: first recover the exact deployed image or original PetaLinux project; rebuilding from the Round30 `.xsa` alone is insufficient to recreate the original board image.
8. User provided the local PetaLinux installation-material directory and asked to continue completing the submission.
   - Inspection result: the directory contains only `plnx-env-setup.sh`, an Ubuntu host-dependency setup script, not the PetaLinux tool installer. Ubuntu 20.04 WSL is present. No PetaLinux 2022.2 installer, BSP/project, `.wic`, `BOOT.BIN`, or `image.ub` was found in the searched locations.
   - Additional verified asset: the 104 MB Vivado `archive_project` ZIP is present locally and its extracted project was opened with Vivado 2026.1; BD validation and IP status reporting completed. It is added as a separate Release asset; implementation run outputs remain excluded.

## Self-check and evidence discipline

- Compared the package scope to AMD guide sections 3.3.2-3.3.5.
- Used the Round20 numeric board report, Round21 audibility rejection, Round23 bounded audible test, Round24 no-speech rejection, and Round30 persistent boot report together.
- Kept the fused minphase kernel claim separate from whole-WORLD acceleration.
- Did not include Round31-34 exploratory synthesis-pulse work as a deployed Round30 feature.
- Did not include audio, bitstreams, PetaLinux images, or build products.
