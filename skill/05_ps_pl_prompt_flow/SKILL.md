---
name: ps-pl-prompt-flow
description: Structure AI-assisted PS/PL work on AMD Zynq projects from requirements and partitioning through HLS/RTL implementation, verification, board testing, and evidence-based review.
---

# PS+PL Prompt Flow

Use this prompt sequence when a Zynq project needs a traceable PS/PL implementation or a controlled iteration on an existing accelerator. The sequence is technology-aware but not tied to speech processing.

Read only the template needed for the current stage:

- [Requirements and partitioning](references/01_requirements_and_partitioning.md)
- [HLS/RTL implementation](references/02_implementation.md)
- [Verification and failure review](references/03_verification_and_failure_review.md)

## Operating rules

- Replace bracketed fields with measured facts. If a field is unknown, label it unknown and state how it can be measured; do not invent a value.
- Keep the requested task scope and acceptance gate explicit. Do not advance from algorithm selection to PL implementation if an earlier quality or functional gate is still open.
- Ask for the smallest useful artifact set: interface contract, current source revision, target part/tool version, baseline test, and relevant logs.
- Change one main variable per experiment. Preserve rejected results and the exact cause or unresolved uncertainty.
- Separate host reference, HLS C simulation, RTL co-simulation, OOC implementation, routed system, board numeric test, live I/O, listening, and stability claims.
- For any physical test that records, plays, or requires an operator, stop before starting until the operator confirms readiness for that specific run.
- Finish with a report containing exact source revision, commands, environment, inputs/hashes, raw evidence, outcome, limits, and next owner.

The prompt templates are a starting point, not proof that the implementation passes. This prompt set is newly assembled from project experience and has not yet been independently forward-tested.
