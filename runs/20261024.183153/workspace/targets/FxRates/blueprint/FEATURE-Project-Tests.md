# FEATURE: Project Test Suite

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Provides the POSIX test runner and automated pytest suite for FxRates. |
| Depends On  | ARCHITECTURE.md, DATABASE.md, FEATURE-CLI-Initialize.md, FEATURE-CLI-Load.md, FEATURE-CLI-Fetch.md, FEATURE-CLI-Serve.md, FEATURE-API-Health.md, FEATURE-API-Statistics.md, FEATURE-API-Rates.md, FEATURE-Conversion.md, FEATURE-History.md |
| Provides    | bin/test.sh |
| Consumes    | fxrates init, fxrates load, fxrates fetch, fxrates serve, GET /health, GET /stats, GET /currencies, GET /rates/{date}, GET /rates/latest, GET /convert, GET /history/{code} |

## Purpose

Provide a project-owned pytest suite and a POSIX-compatible `bin/test.sh` that runs it from the application root and exits zero only when every test passes. The suite exercises commands, validation and atomic loading, fetch with a stubbed download, API behavior, exact arithmetic, and request errors using a temporary database.

## Test coverage

The suite covers each CLI command, valid and invalid CSV rules, no writes after rejected input, duplicate replacement, all API endpoints, effective date selection, conversion and history rounding, and the specified error statuses. Fetch tests replace the downloader with a stub and make no network connection.

## Programmatic Acceptance

=== AC test-runner ===
Intent: The project test runner exits successfully when the completed automated suite passes.

import subprocess

result = subprocess.run(["sh", "bin/test.sh"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC test-runner ===

=== AC test-suite-imports ===
Intent: The declared pytest suite is runnable through the project test command.

import subprocess
import sys

result = subprocess.run([sys.executable, "-m", "pytest", "-q"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC test-suite-imports ===

## User Acceptance

- None.

## Guardrails

- Tests stub fetch downloads and never use the network.
- Keep the runner POSIX-compatible.
- Do not modify or replace supplied files under `sources/`.
