# BIG ERRORS — action required

- Command: `plan`
- Phase: plan verify
- State: Error
- Timestamp: 2026-10-24T15:58:43+00:00
- Execution ID: 20261024.155418.200Z-8ba7b8dd
- Challenge Execution ID: -
- Classification: plan cannot be built as written
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.155325/workspace/logs

## Diagnostic

plan verify: FxRates
  3 criteria cannot run as written
  ✗  FEATURE-LOAD.md [load-valid-fixture]: Cite: sources/INSTRUCTIONS.md:8-10 sources/run.sh:86-94 does not resolve to lines of a file under sources/; cite sources/<file>:<line> or sources/<file>:<start>-<end>
  ✗  FEATURE-LOAD.md [load-invalid-atomic]: Cite: sources/INSTRUCTIONS.md:39-42 sources/run.sh:95-95 does not resolve to lines of a file under sources/; cite sources/<file>:<line> or sources/<file>:<start>-<end>
  ✗  ARCHITECTURE.md [architecture-imports]: imports `persistence`, which Drydock generates from DATABASE.md at block 2 (story `database`), after story `architecture-foundation` builds at block 1; assert only what that story delivers and leave persistence to DATABASE.md's criteria
  ⚠  FEATURE-LOAD.md [load-valid-fixture]: captures a program's output and prints none of it; print its pass/fail counts before asserting so repair can see progress
  ⚠  FEATURE-LOAD.md [load-invalid-atomic]: captures a program's output and prints none of it; print its pass/fail counts before asserting so repair can see progress
  ⚠  FEATURE-LOAD.md [load-repeat]: captures a program's output and prints none of it; print its pass/fail counts before asserting so repair can see progress
  Run: drydock plan repair FxRates

## Recovery

Run: drydock plan repair FxRates
