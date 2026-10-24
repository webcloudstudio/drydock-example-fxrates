# STOP

- stage: initial-build-1
- declared: 2026-10-24T07:08:15Z

## Reason

The build exited 1 with work still on the frontier. Diagnose the failing block from its evidence before rerunning; a score taken over a partial build grades the absence, not the product.

## Clearing

Fix the cause, then delete this file, or answer `y` when an interactive Drydock command
offers to clear it. Every LLM-assisted command refuses to run while it exists, so a run
that continues past a halt cannot be produced by accident.
