# BIG ERRORS — action required

- Command: `build`
- Phase: build step
- State: Failed
- Timestamp: 2026-10-25T20:36:50+00:00
- Execution ID: 20261025.203415.422Z-f3607ee6
- Challenge Execution ID: -
- Classification: programmatic acceptance failed: conversion-route
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/workspace/targets/FxRates/evidence/block-3.md

## Diagnostic

Block "Block 3 · Service" [block-3] failed its acceptance criteria.
  Story "Convert amounts between currencies using exact decimal arithmetic." [api-003] does not meet its own acceptance criteria:
    - AC conversion-route — Conversion returns a reachable response with the supplied amount and currencies using the effective stored rates.
        assertion: assert body["result"] == "10.00" → AssertionError
        raised at: conversion-route.py:25
        process exit code: 1
        values at failure:
          body = {'date': '2099-01-02', 'from': 'XTS', 'to': 'XTU', 'amount': '2.00', 'rate': '2.500000', 'result': '5.00'}
        check stderr:
… (7 more lines truncated)

## Recovery

The agent disputes failing acceptance criteria; the claim is unverified.
Run: drydock plan verify FxRates
  Inspect the criteria and evidence before rebuilding.
Run: drydock plan repair FxRates
  Repair confirmed mechanical defects, then verify before rebuilding.
