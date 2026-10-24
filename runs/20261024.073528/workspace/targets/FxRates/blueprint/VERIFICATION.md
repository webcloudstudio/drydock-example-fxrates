# FEATURE: Full Verification

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Gates the completed application on the supplied full conformance grader. |
| Depends On  | FEATURE-Rate-Loading.md, FEATURE-CLI.md, FEATURE-API-Overview.md, FEATURE-Rate-Queries.md, FEATURE-Currency-Conversion.md, FEATURE-Currency-History.md, FEATURE-Rate-Fetch.md, FEATURE-Test-Suite.md |
| Provides    | full conformance verification |

## Purpose

Run the supplied grader from the completed application root as the terminal verification gate. It loads the staged ECB fixtures, launches the executable and API, and exercises the complete command and HTTP behavior. Its exit status is the verdict.

## Programmatic Acceptance

=== AC full-conformance ===
Intent: The supplied FxRates grader passes all 35 checks.
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
=== END AC full-conformance ===

## User Acceptance

- None.

## Guardrails

- Run the staged grader unmodified from the application root.
- Treat its exit status as the full verification verdict.
