# BIG ERRORS — action required

- Command: `build`
- Phase: managed state verification
- State: Error
- Timestamp: 2026-10-27T19:36:28+00:00
- Execution ID: 20261027.193228.463Z-05a4d299
- Challenge Execution ID: -
- Classification: managed-state violation
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/workspace/targets/FxRates/evidence/block-4.md

## Diagnostic

Managed SQLite state changed during agent execution. Retained pre-call snapshot: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/workspace/targets/FxRates/evidence/managed-state/sqlite-2rqgxlo6/app.db. Review and restore through the persistence owner before continuing; no automatic overwrite or reprovisioning was performed.

## Recovery

Review persistence evidence and restore the configured store through DATABASE story `database`.
Preserve existing data and any retained managed-state snapshot; provisioning an empty store is not data recovery.
Managed SQLite state changed during agent execution. Retained pre-call snapshot: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/workspace/targets/FxRates/evidence/managed-state/sqlite-2rqgxlo6/app.db. Review and restore through the persistence owner before continuing; no automatic overwrite or reprovisioning was performed.
After the store is restored and verified, run: drydock build FxRates
