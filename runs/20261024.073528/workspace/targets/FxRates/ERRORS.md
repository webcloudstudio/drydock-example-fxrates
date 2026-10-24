# BIG ERRORS — action required

- Command: `build`
- Phase: LLM execution
- State: Error
- Timestamp: 2026-10-24T07:42:43+00:00
- Execution ID: 20261024.074110.972Z-9790f444
- Challenge Execution ID: -
- Classification: persistence verification failed
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.073528/workspace/targets/FxRates/evidence/block-1.md

## Diagnostic

persistence artifacts missing; rebuild the DATABASE step

## Recovery

Inspect the execution evidence, correct the execution issue, then run: drydock build FxRates --step block-1

## Diagnosis

CAUSE: `DATABASE` produced no persistence artifacts, so block-1 acceptance could not verify the app or database interface.
DO: Inspect `persistence/` and rebuild the `DATABASE` step to generate its artifacts.
DO: Run `drydock build FxRates --step block-1`.
