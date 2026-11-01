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

## Self-check and evidence discipline

- Compared the package scope to AMD guide sections 3.3.2-3.3.5.
- Used the Round20 numeric board report, Round21 audibility rejection, Round23 bounded audible test, Round24 no-speech rejection, and Round30 persistent boot report together.
- Kept the fused minphase kernel claim separate from whole-WORLD acceleration.
- Did not include Round31-34 exploratory synthesis-pulse work as a deployed Round30 feature.
- Did not include audio, bitstreams, PetaLinux images, or build products.
