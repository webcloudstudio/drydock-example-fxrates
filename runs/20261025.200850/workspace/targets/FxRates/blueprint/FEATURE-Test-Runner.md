# FEATURE: Test Runner

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Defines the project test suite and its POSIX runner. |
| Depends On  | ARCHITECTURE.md |
| Provides    | bin/test.sh, pytest suite |
| Consumes    | fxrates init, fxrates load, fxrates fetch, fxrates serve, GET /health, GET /stats, GET /currencies, GET /rates/{date}, GET /rates/latest, GET /convert, GET /history/{code} |

## Purpose

Provide a repeatable local test command for the application. The suite exercises the CLI and HTTP API against temporary database files and stubs the fetch downloader so tests never use the network.

## Test Runner

- `bin/test.sh` is a POSIX-compatible shell script run from the application root.
- It invokes pytest for the project suite and returns zero only if every test passes.
- The pytest suite covers every CLI command, each file-loading rule, each API endpoint, effective publication dates, conversion and history rounding, and declared error statuses.
- Tests use FastAPI `TestClient` and a real temporary SQLite database. Fetch tests replace the downloader with a stub.

## Programmatic Acceptance

=== AC test-runner-exits-successfully ===
Intent: The declared pytest test command completes successfully.

import subprocess

result = subprocess.run(
    ["sh", "bin/test.sh"],
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC test-runner-exits-successfully ===

## User Acceptance

- None.

## Guardrails

- Tests must not open a network connection; fetch behavior is tested with a stubbed downloader.
- Keep the test runner POSIX-compatible and run the suite from the application root.
- The script exits zero only when every automated test passes.
