# Stage 2: HLS/RTL Implementation

Use after the interface and acceptance contract have been reviewed and frozen.

```text
Implement only the accepted PS/PL boundary below.

Target: [exact AMD part]
Tool version: [Vivado/Vitis]
Source revision and owned paths: [SHA and file list]
Interface contract: [frozen types, sizes, units, scaling, register/DMA map]
Reference function: [trusted software implementation and version]
Acceptance: [numeric tolerance, resource/timing limits, timeout behavior]
Existing scripts/tests: [paths]

First inspect the relevant code and report dependencies or contradictions. Then make the smallest implementation change. Preserve PS fallback behavior only if the frozen contract calls for it. Add or update a deterministic testbench using fixed or reproducibly generated vectors. Do not include generated build products, bitstreams, models, or human audio in source control unless the project explicitly requires them.

Return:
- changed paths and why each is necessary;
- build/simulation commands and exact expected outputs;
- interface and scaling assumptions that need confirmation;
- tests not run and why;
- evidence needed before calling this a board pass.
```

For an existing design, ask the model to inspect the source and build scripts before it edits. In this project, the WORLD 0.3.5 tree and generated full audio project were external inputs, so the checked-in Tcl alone was not a clean-room full-system build.
