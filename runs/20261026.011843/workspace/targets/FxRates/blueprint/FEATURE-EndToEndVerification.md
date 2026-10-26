# FEATURE: End-to-End Verification

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Runs the supplied grader as the terminal full-application acceptance gate. |
| Depends On  | FEATURE-DatabaseInitialization.md, FEATURE-HistoryLoading.md, FEATURE-HistoryFetch.md, FEATURE-ServiceOverview.md, FEATURE-EffectiveRates.md, FEATURE-CurrencyConversion.md, FEATURE-CurrencyHistory.md, FEATURE-TestRunner.md |
| Provides    | sources/run.sh |

## Purpose

The staged grader is the final end-to-end verification of the complete CLI and HTTP service.

## Behavior

- Run `sh sources/run.sh` from the completed application root.
- Require its exit status to be zero; the grader owns the complete expected behavior and reports its own diagnostics.
- The grader uses only local HTTP requests and staged fixtures; it does not invoke fetch.

## Programmatic Acceptance

=== AC supplied-grader ===
Intent: The supplied end-to-end grader passes the complete application.
Suite: full

Requires: executable=sh; scope=test

import subprocess

result = subprocess.run(
    ["sh", "sources/run.sh"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC supplied-grader ===

## User Acceptance

- None.

## Guardrails

- Do not modify or replace `sources/run.sh` or its supplied data assets.
- Do not run the grader before all implementation stories are complete.
- The grader's exit status is the verdict; output is diagnostic.
