# FEATURE: Release Verification

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines the final verification run for the completed FxRates application. |
| Depends On  | ARCHITECTURE.md, FEATURE-CLI-Init.md, FEATURE-CLI-Load.md, FEATURE-CLI-Errors.md, FEATURE-CLI-Fetch.md, FEATURE-API-Health-Stats.md, FEATURE-API-Currencies.md, FEATURE-API-Rates.md, FEATURE-API-Convert.md, FEATURE-API-History.md, FEATURE-API-Validation.md, FEATURE-CLI-Serve.md |
| Provides    | Full supplied FxRates conformance verification |

## Purpose

Run the supplied conformance harness as the terminal verification of the completed application. The harness initializes a fresh database, loads the supplied ECB fixtures, starts the service, and checks CLI behavior and HTTP responses. Its exit status is the verdict.

## Verification

The authoritative suite is staged at `sources/run.sh`. Run it from the application root with `sh sources/run.sh` after all implementation stories have completed. Do not alter the harness or its fixtures.

## Programmatic Acceptance

=== AC full-conformance ===
Intent: The completed application passes the supplied full FxRates conformance harness.
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

- Do not modify, rewrite, regenerate, or substitute any file under `sources/`.
- This verification runs only after every implementation story is complete.
- The harness exit status is the acceptance signal; captured output is diagnostic only.
