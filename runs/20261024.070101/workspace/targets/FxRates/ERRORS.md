# BIG ERRORS — action required

- Command: `build`
- Phase: build step
- State: Failed
- Timestamp: 2026-10-24T07:08:08+00:00
- Execution ID: -
- Challenge Execution ID: -
- Classification: programmatic acceptance failed: rates-delete
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/workspace/targets/FxRates/evidence/block-2.md

## Diagnostic

Block "Block 2 · Foundational" [block-2] failed its acceptance criteria.
  Story "Declare the rates schema and repository contract." [database] does not meet its own acceptance criteria:
    - AC rates-delete — The rates delete operation removes only the row selected by its date and currency key.
        assertion: persistence.db.PersistenceError: FEATURE-RATE-003 failed: FieldType.__init__() missing 2 required positional arguments: 'id' and 'rate'
        raised at: db.py:398
        process exit code: 1
        error: persistence.db.PersistenceError: FEATURE-RATE-003 failed: FieldType.__init__() missing 2 required positional arguments: 'id' and 'rate'
        values at failure:
… (23 more lines truncated)

## Recovery

Run: drydock build FxRates
  to continue the build. This story resumes where it left off and is retried against the checks it failed.
