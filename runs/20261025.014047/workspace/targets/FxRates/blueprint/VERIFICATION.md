# FEATURE: Release Verification

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Runs the supplied end-to-end grader as the terminal release verification. |
| Depends On  | ARCHITECTURE.md, DATABASE.md, FEATURE-CLI-INIT.md, FEATURE-CLI-LOAD.md, FEATURE-CLI-FETCH.md, FEATURE-API-HEALTH-STATS.md, FEATURE-API-CURRENCIES.md, FEATURE-API-RATES.md, FEATURE-API-CONVERT.md, FEATURE-API-HISTORY.md, FEATURE-API-REFERENCE.md, FEATURE-TEST-SUITE.md |

## Programmatic Acceptance

=== AC supplied-grader ===
Intent: The supplied end-to-end grader passes against the completed application.
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
=== END AC supplied-grader ===

## User Acceptance

- None.

## Guardrails

- Treat `sources/run.sh` as a read-only authoritative grader; do not modify or substitute it.
- Do not reproduce its known answers in hand-authored assertions.
