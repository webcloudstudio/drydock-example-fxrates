# FEATURE: Test Runner

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Provides the offline POSIX test command for the project’s pytest suite. |
| Depends On  | FEATURE-HistoryFetch.md, FEATURE-ServiceOverview.md, FEATURE-EffectiveRates.md, FEATURE-CurrencyConversion.md, FEATURE-CurrencyHistory.md |
| Provides    | bin/test.sh |

## Purpose

Provide one command that runs the application's pytest suite from the project root. It succeeds only when pytest reports the complete suite passes.

## Behavior

- `bin/test.sh` is POSIX-compatible and runs pytest from the application root.
- The suite covers CLI commands and load validation, all API endpoints, effective-date resolution, Decimal rounding, and error statuses.
- Fetch tests replace the downloader with a stub. The automated test suite makes no network connection.

## Programmatic Acceptance

=== AC test-runner-exits-successfully ===
Intent: The project test runner exits successfully when run from the application root after implementation stories are complete.

Requires: executable=sh; scope=test

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

- Do not permit automated tests to contact the ECB or any other network host.
- Keep the runner POSIX-compatible.
