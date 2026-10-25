# FEATURE: Automated Test Suite

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Provides a POSIX test runner and pytest coverage for the command-line and HTTP service. |
| Depends On  | ARCHITECTURE.md, FEATURE-CLI-INIT.md, FEATURE-CLI-LOAD.md, FEATURE-CLI-FETCH.md, FEATURE-API-HEALTH-STATS.md, FEATURE-API-CURRENCIES.md, FEATURE-API-RATES.md, FEATURE-API-CONVERT.md, FEATURE-API-HISTORY.md, FEATURE-API-REFERENCE.md |
| Provides    | bin/test.sh, pytest suite |

## Purpose

Provide a POSIX-compatible `bin/test.sh` that runs the project's pytest suite from the application root and returns success only when all tests pass. The suite covers each command and load rule, each API endpoint, effective-date resolution, rounding, and error statuses.

Fetch tests replace the download with a stub. Automated tests must not open network connections.

## Programmatic Acceptance

=== AC test-runner-passes ===
Intent: The project test runner completes successfully after the command and API capabilities are implemented.
Requires: python-package=pytest; scope=test

import subprocess

result = subprocess.run(
    ["sh", "bin/test.sh"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC test-runner-passes ===

## User Acceptance

- None.

## Guardrails

- Keep the runner POSIX-compatible and run tests from the application root.
- Stub ECB downloads in tests; tests must not use the network.
- The runner exits zero only when every automated test passes.
