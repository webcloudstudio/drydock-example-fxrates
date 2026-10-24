# BIG ERRORS — action required

- Command: `plan`
- Phase: post-output validation
- State: Error
- Timestamp: 2026-10-24T16:23:58+00:00
- Execution ID: 20261024.162119.398Z-1fdc78de
- Challenge Execution ID: -
- Classification: plan generation stalled
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.162029/workspace/logs

## Diagnostic

Blueprint generation stalled after TOPOLOGY.md was accepted and frozen, after 3 Stage 2 pass(es).
  last rejection: DATABASE.md does not parse: DATABASE.md: FEATURE-RATE-001 Match names `date`, `currency`, which are not Input fields. Every Match field is an Input field the caller supplies.
  last rejection: DATABASE.md: FEATURE-RATE-002 Match names `date`, which is not Input fields. Every Match field is an Input field the caller supplies.
  last rejection: DATABASE.md: FEATURE-RATE-005 declares `rates.by_date`, which FEATURE-RATE-002 already declares. An operation name is one method, `db.rates.by_date(...)`; give this one its own name and `| Kind |`, or merge the two patterns.
… (19 more lines truncated)

## Recovery

Inspect the failed Stage 2 batch, then run: drydock plan FxRates
