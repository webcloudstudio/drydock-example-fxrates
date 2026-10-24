# BIG ERRORS — action required

- Command: `build`
- Phase: build step
- State: Failed
- Timestamp: 2026-10-24T14:59:34+00:00
- Execution ID: -
- Challenge Execution ID: -
- Classification: programmatic acceptance failed: rates-upsert
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.145257/workspace/targets/FxRates/evidence/block-2.md

## Diagnostic

Block "Block 2 · Foundational" [block-2] failed its acceptance criteria.
  Story "Declare the rates schema and persistence operations." [database-contract] does not meet its own acceptance criteria:
    - AC rates-upsert — Upserting a rate stores its published text and replaces the matching date and currency row.
        assertion: failed with no diagnostic output
        raised at: db.py:214
        process exit code: 1
        values at failure:
          name = 'get'
          granted = 'list_all, list_currency, list_date, upsert'
          self = <TableAccess rates: list_all, list_currency, list_date, upsert>
        check stderr:
          Traceback (most recent call last):
            File "rates-upsert.py", line 9, in <module>
… (5 more lines truncated)

## Recovery

Run: drydock build FxRates
  to continue the build. This story resumes where it left off and is retried against the checks it failed.
