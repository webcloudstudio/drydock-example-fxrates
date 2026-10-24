# FEATURE: Automated Test Suite

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Provides a network-free pytest suite and POSIX test runner for FxRates. |
| Depends On  | FEATURE-CLI.md, FEATURE-API-FOUNDATION.md |
| Provides    | bin/test.sh, pytest suite |
| Consumes    | fxrates commands, application API |

## Purpose

Provide `bin/test.sh` to run the project's pytest suite from the application root, returning zero only when the suite passes. The suite uses a real temporary database and FastAPI `TestClient`, covers each command and endpoint, load validation and atomicity, effective-date behavior, Decimal rounding, and error statuses. Stub the fetch download so tests do not use the network.

## Programmatic Acceptance

=== AC test-runner-exits-successfully ===
Intent: The project test runner exits successfully after the complete implementation is available.
Requires: executable=sh; scope=test

import subprocess

result = subprocess.run(["sh", "bin/test.sh"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC test-runner-exits-successfully ===

## User Acceptance

- None.

## Guardrails

- Tests must not open a network connection.
- `bin/test.sh` must be POSIX-compatible.
