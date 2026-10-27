# Blockers: Uat Stage
- target: FxRates
- source: drydock uat FxRates
- declared: 2026-10-27T15:36:35-04:00

<!-- drydock-state: {"owner": "uat FxRates", "execution": "", "attempts": 1} -->

## blocker-001: initial-build-1
- kind: environmental
- class: uat stage
- auto-continue: no

### Error

drydock build FxRates exited 1.

stderr:
error: build failed for FxRates: 4 step(s)
  cli-init — closed/failed: managed-state violation

Evidence:
  stderr: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/evidence/commands/10-initial-build-1.stderr.log
  stdout: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/evidence/commands/10-initial-build-1.stdout.log

### Why blocked

The build did not complete. UAT stopped before acceptance tests and scoring because the application is unfinished. Resolve the build error above before rerunning UAT.
