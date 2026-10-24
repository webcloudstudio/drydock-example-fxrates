# FEATURE: Full Grader Verification

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Verifies the completed application against the supplied FxRates grader. |
| Depends On  | FEATURE-TESTS.md |
| Provides    | Full supplied grader verification |
| Consumes    | sources/run.sh |

## Purpose

The terminal verification story runs the supplied grader after all implementation stories have completed. Its exit status is the acceptance verdict. The grader is staged verbatim and must not be modified.

## Programmatic Acceptance

=== AC supplied-grader-full-suite ===
Intent: The complete supplied grader passes after implementation is complete.
Suite: full
Requires: executable=sh; scope=test

import subprocess

result = subprocess.run(["sh", "sources/run.sh"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC supplied-grader-full-suite ===

## User Acceptance

- None.

## Guardrails

- Do not modify or replace `sources/run.sh` or the supplied CSV fixtures.
- Application code must not read or embed answers from the grader.
