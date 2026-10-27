# FEATURE: Release Verification

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | The supplied grader sources/run.sh passes end to end against the completed fxrates application. |
| Depends On | FEATURE-InitCommand.md, FEATURE-CommandHelp.md, FEATURE-OfflineTestRun.md, FEATURE-LoadVisibility.md, FEATURE-Fetch.md, FEATURE-Currencies.md, FEATURE-RatesLatest.md, FEATURE-ConvertErrors.md, FEATURE-HistoryErrors.md |
| Provides | release verification |
| Consumes | fxrates init, fxrates load, fxrates serve, GET /health, GET /stats, GET /currencies, GET /rates/{date}, GET /rates/latest, GET /convert, GET /history/{code} |

## Purpose

Assembly and intent only. Every behavior is implemented by earlier stories. This story runs the
supplied grader `sources/run.sh`, unmodified and unfiltered, from the application root. The
script's exit status is the verdict: it loads the supplied ECB files, starts `fxrates serve` on a
free local port, and makes 35 checks of command output and HTTP status and JSON body.

## Behavior

- The grader and its data files under `sources/` are read-only scoring assets and are never
  modified, regenerated, or substituted.
- Application code never reads `sources/run.sh` or the supplied data files.
- A nonzero exit means a check failed; the printed `FAIL` lines identify it.

## Programmatic Acceptance

=== AC grader-passes ===
Intent: The complete supplied grader exits zero, which means every one of its checks passed against the built application.
Suite: full
Requires: executable=sh; scope=test
Requires: executable=python3; scope=test

import subprocess
import sys

result = subprocess.run(
    ["sh", "sources/run.sh"],
    capture_output=True,
    text=True,
    timeout=900,
)
print(result.stdout)
print(result.stderr, file=sys.stderr)
assert result.returncode == 0
=== END AC grader-passes ===

## User Acceptance

- None.

## Guardrails

- Do not modify, rewrite, regenerate, or substitute any file under `sources/`.
- Do not filter, skip, or reinterpret any check in `sources/run.sh`.
- The only verdict is the grader's exit status.
