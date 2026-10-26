# BIG ERRORS — action required

- Command: `build`
- Phase: build step
- State: Failed
- Timestamp: 2026-10-25T23:18:29+00:00
- Execution ID: 20261025.231658.095Z-dfe7e129
- Challenge Execution ID: -
- Classification: programmatic acceptance failed: rates_list_filters_and_order
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.230142/workspace/targets/FxRates/evidence/block-2.md

## Diagnostic

Block "Block 2 · Foundational" [block-2] failed its acceptance criteria.
  Story "Declare the rates store and repository operations." [database] does not meet its own acceptance criteria:
    - AC rates_list_filters_and_order — List stored rates in date and currency order and filter by currency and inclusive date bounds.
        assertion: assert [(row.date, row.currency, row.rate) for row in all_rows if row.date in dates] == [ → AssertionError
        raised at: rates_list_filters_and_order.py:20
        process exit code: 1
        values at failure:
… (10 more lines truncated)

## Recovery

The agent disputes failing acceptance criteria; the claim is unverified.
Run: drydock plan verify FxRates
  Inspect the criteria and evidence before rebuilding.
Run: drydock plan repair FxRates
  Repair confirmed mechanical defects, then verify before rebuilding.
