# FEATURE: Verification Suite

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Provides a pytest suite and POSIX runner for application behavior, with fetch downloads stubbed. |
| Depends On  | ARCHITECTURE.md, DATABASE.md, FEATURE-API-Foundation.md, FEATURE-CLI-Foundation.md |
| Provides    | bin/test.sh, pytest suite |

## Purpose

Provide an application-owned automated suite, run by `sh bin/test.sh` from the application root, that exits zero only when every project test passes.

## Coverage

The suite covers every command, each CSV loading rule, each HTTP endpoint, effective-date behavior, decimal rounding, and each specified error status. It uses a real temporary database for project tests. Fetch tests replace the download with a stub and never make a network connection.

## Programmatic Acceptance

=== AC project-test-runner ===
Intent: The project's POSIX test runner exits zero after running the complete automated suite.

import subprocess

result = subprocess.run(["sh", "bin/test.sh"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC project-test-runner ===

=== AC fetch-tests-stub-network ===
Intent: The automated suite passes with fetch covered by stubbed downloads and no network access.

import subprocess

result = subprocess.run(["sh", "bin/test.sh"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC fetch-tests-stub-network ===

## User Acceptance

- None.

## Guardrails

- `bin/test.sh` is POSIX-compatible and runs pytest from the application root.
- Tests must stub fetch downloads; automated tests do not open a network connection.
- The suite uses a real temporary database and covers the stated command, loader, API, arithmetic, and error behavior.
