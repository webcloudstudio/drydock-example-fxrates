# Blockers: Uat Stage
- target: FxRates
- source: drydock uat FxRates
- declared: 2026-10-25T16:36:57-04:00

<!-- drydock-state: {"owner": "uat FxRates", "execution": "", "attempts": 1} -->

## blocker-001: initial-build-1
- kind: environmental
- class: uat stage
- auto-continue: no

### Error

drydock build FxRates exited 1.

stderr:
error: build failed for FxRates: 9 step(s)
  ecb-001 — closed/failed: programmatic acceptance failed: conversion-route

Evidence:
  stderr: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/evidence/commands/10-initial-build-1.stderr.log
  stdout: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/evidence/commands/10-initial-build-1.stdout.log

### Why blocked

The build did not complete. UAT stopped before acceptance tests and scoring because the application is unfinished. Resolve the build error above before rerunning UAT.
