# FEATURE: Complete Grader Verification

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Defines the terminal verification of the supplied FxRates grader. |
| Depends On  | ARCHITECTURE.md, DATABASE.md, FEATURE-AppServer.md, FEATURE-CLI.md, FEATURE-Load.md, FEATURE-Fetch.md, FEATURE-Init.md, FEATURE-Health.md, FEATURE-Stats.md, FEATURE-Currencies.md, FEATURE-Rates.md, FEATURE-LatestRates.md, FEATURE-Convert.md, FEATURE-History.md, FEATURE-CLI-Errors.md, FEATURE-Tests.md |
| Provides    | complete supplied grader verification |
| Consumes    | sources/run.sh |

## Purpose

Run the supplied grader after all implementation and project test work is complete. The grader's exit status is the release verification result.

## Verification

- Invoke the staged `sources/run.sh` from the application root without modifying or filtering it.
- Treat its exit status as the sole acceptance verdict.

## Programmatic Acceptance

=== AC grader-complete ===
Intent: The complete supplied grader passes.
Suite: full

import subprocess

result = subprocess.run(
    ["sh", "sources/run.sh"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC grader-complete ===

## User Acceptance

- None.

## Guardrails

- Keep `sources/run.sh` and all supplied scoring assets unchanged.
- Run the full grader only as terminal project verification.
