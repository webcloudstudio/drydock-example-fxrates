# BIG ERRORS — action required

- Command: `build`
- Phase: build step
- State: Failed
- Timestamp: 2026-10-24T05:43:46+00:00
- Execution ID: 20261024.054026.852Z-038863a6
- Challenge Execution ID: -
- Classification: programmatic acceptance failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit-rate
- Evidence / logs: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.051856/workspace/targets/FxRates/evidence/block-3.md

## Diagnostic

Block "Block 3 · Service" [block-3] failed its acceptance criteria.
  Story "Return bounded currency history and summary statistics." [api_005] does not meet its own acceptance criteria:
    - AC history-route-empty-range — A currency with stored history returns the declared empty summary for a range with no points.
        assertion: assert response.status_code == 200 → AssertionError
        raised at: history-route-empty-range.py:11
        process exit code: 1
        values at failure:
          response = <Response [404 Not Found]>
        check stderr:
          /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
… (52 more lines truncated)

## Recovery

Run: drydock build FxRates
  to continue the build. This story resumes where it left off and is retried against the checks it failed.
