# BIG ERRORS — action required

- Command: `build`
- Phase: managed state verification
- State: Error
- Timestamp: 2026-10-27T17:11:26+00:00
- Execution ID: 20261027.170854.522Z-c29cd1c4
- Challenge Execution ID: -
- Classification: managed-state violation
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/workspace/targets/FxRates/evidence/block-16.md

## Diagnostic

Managed SQLite state changed during agent execution. Retained pre-call snapshot: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/workspace/targets/FxRates/evidence/managed-state/sqlite-e5ov3t78/app.db. Review and restore through the persistence owner before continuing; no automatic overwrite or reprovisioning was performed.

## Recovery

Review persistence evidence and restore the configured store through DATABASE story `database`.
Preserve existing data and any retained managed-state snapshot; provisioning an empty store is not data recovery.
Managed SQLite state changed during agent execution. Retained pre-call snapshot: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/workspace/targets/FxRates/evidence/managed-state/sqlite-e5ov3t78/app.db. Review and restore through the persistence owner before continuing; no automatic overwrite or reprovisioning was performed.
After the store is restored and verified, run: drydock build FxRates
