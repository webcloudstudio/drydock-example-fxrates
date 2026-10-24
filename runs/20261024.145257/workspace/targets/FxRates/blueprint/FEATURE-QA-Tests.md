# FEATURE: QA Tests

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Provides a POSIX test runner and pytest suite for FxRates. |
| Depends On  | ARCHITECTURE.md, FEATURE-CLI-Init.md, FEATURE-CLI-Load.md, FEATURE-CLI-Fetch.md, FEATURE-CLI-Serve.md, FEATURE-API-Overview.md, FEATURE-API-Rates.md, FEATURE-API-Convert.md, FEATURE-API-History.md |
| Provides    | bin/test.sh |
| Consumes    | fxrates init, fxrates load, fxrates fetch, fxrates serve, GET /health, GET /stats, GET /currencies, GET /rates/{date}, GET /rates/latest, GET /convert, GET /history/{code} |

## Purpose

Provide an automated pytest suite runnable from the application root through `bin/test.sh`. The suite exercises the CLI and JSON API using real temporary SQLite databases and FastAPI's `TestClient`. Fetch tests replace the downloader with a stub; tests make no network connections.

## Test coverage

The suite covers each CLI command and its relevant usage and operational errors; complete-file validation, atomic rejection, replacement, and published-text preservation for ECB loads; all API routes, empty and populated database responses, effective-date fallback, conversion and history rounding, malformed inputs, unknown currencies, and visibility of a completed load to the next request.

`bin/test.sh` is POSIX-compatible, runs pytest from the application root, and returns success only when the suite passes.

## Programmatic Acceptance

=== AC test-runner ===
Intent: The declared test runner exists and executes pytest successfully.

from pathlib import Path
import subprocess

runner = Path("bin/test.sh")
assert runner.is_file()
result = subprocess.run(["sh", str(runner)], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC test-runner ===

## User Acceptance

- None.

## Guardrails

- Tests must use temporary databases and must not connect to the network.
- Fetch tests replace the download with a stub.
- Do not modify files under `sources/`.
