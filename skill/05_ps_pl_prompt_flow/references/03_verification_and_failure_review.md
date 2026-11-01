# Stage 3: Verification and Failure Review

Use one prompt per verification level. Do not combine evidence from different levels into one acceptance claim.

## Regression prompt

```text
Review this test result against the frozen contract.

Source SHA: [full SHA]
Test level: [host / HLS C simulation / RTL co-simulation / OOC / routed system / board numeric / live I/O / listening / stability]
Tool/board: [versions and exact part]
Input identity: [vector/audio identifiers and hashes; do not attach controlled media unless required]
Reference and candidate builds: [exact commands and hashes]
Acceptance threshold: [numeric rule]
Observed result: [raw values and evidence paths]

Determine pass, reject, blocked, or invalid trial. Check normalization/scaling, input identity, fallback counters, timeouts, output energy, and test duration where applicable. Identify whether the failure is in the design, tool setup, test harness, input preparation, or evidence. Propose one next change only. Do not infer audible output from nonzero samples or stability from a no-speech run.
```

## Physical test prompt

```text
Prepare a bounded physical test plan only; do not start capture or playback.

Operator readiness for this exact run: [confirmed / not confirmed]
Board and recovery baseline: [exact IDs and hashes]
Candidate files/hashes: [exact list]
Test purpose and stop condition: [one question]
Input/output setup: [microphone/speaker, sample format, duration]
Expected result and rollback: [specific]

Check that the proposed run does not overlap another owner, alter unverified boot assets, or skip required recovery. If readiness is not confirmed, stop at the plan. List the exact observations to save and post-test restoration checks.
```

## Round report prompt

```text
Write a concise report for this single implementation or test round.

Task ID/date/role: [values]
Baseline and resulting source SHA: [full hashes]
Changed paths/commands: [exact]
Environment/input identity: [versions, formats, hashes]
Raw evidence: [paths and hashes]
Measured result: [values and count/duration]
Decision: [PROPOSED / ACCEPTED / REJECTED / BLOCKED]
Known limits: [claims not established]
Next owner/action: [one]

Preserve prior failures and verbatim user listening feedback. State the exact proof level. Do not call a round complete if its stated exit gate is still open.
```

These prompts capture recurring lessons from the project: a Round21 live run had zero digital underruns but was rejected when no sound was heard; Round24's 60-second run had zero voiced frames and was invalid as speech stability evidence; Round30 proved persistent boot and active PL calls but did not prove long-duration speech stability.
