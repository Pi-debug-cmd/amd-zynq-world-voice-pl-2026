# Stage 1: Requirements and Partitioning

Use before proposing a PS/PL boundary.

```text
Act as the design reviewer for this AMD Zynq project.

Goal: [user-visible function and target acceptance]
Board/part: [exact board and part]
OS/tool versions: [PS OS, Vivado/Vitis versions]
Current source revision: [full commit SHA]
Input/output contract: [formats, rates, dimensions, timing]
Measured baseline: [profile or reference data, with evidence paths]
Constraints: [latency, resources, power, memory, licensing, offline/online]
Open gates and ownership: [current status and responsible person]

Using only those facts and the attached source/evidence:
1. Restate the measurable acceptance criteria and identify missing facts.
2. Identify the measured bottleneck; distinguish profiling data from assumption.
3. Compare PS-only, PL-offload, and any justified alternative.
4. Recommend the smallest hardware boundary that can be measured against a golden reference.
5. Specify its input/output types, units, scaling, memory ownership, registers/DMA, timeout/fallback behavior, and error budget.
6. Give a one-variable experiment and the exact evidence needed to accept or reject it.

Do not write implementation code yet. Do not claim a performance gain or board capability that is not in the supplied evidence. If a preceding quality or functional gate is open, say whether PL work should wait.
```

Before implementation, compare the result with the actual task owner and project rules. In the WORLD Round30 work, only the fixed minimum-phase stage was in the deployed PL candidate; profiling other WORLD stages did not make them part of that candidate.
