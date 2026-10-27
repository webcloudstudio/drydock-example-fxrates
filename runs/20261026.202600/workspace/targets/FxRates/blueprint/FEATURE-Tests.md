# FEATURE: Offline Automated Tests

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Defines the offline pytest suite and its POSIX test launcher. |
| Depends On  | FEATURE-CLI.md, FEATURE-AppServer.md, FEATURE-Load.md, FEATURE-Fetch.md, FEATURE-Init.md, FEATURE-Health.md, FEATURE-Stats.md, FEATURE-Currencies.md, FEATURE-Rates.md, FEATURE-LatestRates.md, FEATURE-Convert.md, FEATURE-History.md, FEATURE-CLI-Errors.md |
| Provides    | bin/test.sh |
| Consumes    | ./fxrates, cli.testing.cli_runner(), app_server.testing.web_client(), rates repository operations |

## Purpose

Provide a project-owned automated suite that runs locally without network access and exercises the command-line and HTTP product behavior against a real temporary database.

## Behavior

- `bin/test.sh` is a POSIX-compatible launcher, runs pytest from the application root, and exits zero only when the full suite passes.
- The suite covers each command, CSV validation and atomicity rules, each API endpoint, effective-date lookup, decimal rounding, and error statuses.
- Fetch tests stub the download operation. Include both a successful archive download and load and an operational download failure returning status 1.
- Use `cli.testing.cli_runner()` for in-process CLI behavior and `app_server.testing.web_client()` for API behavior.
- Keep tests deterministic and offline; do not make network calls.

## Programmatic Acceptance

=== AC test-suite-passes ===
Intent: The project's test launcher completes successfully.
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
=== END AC test-suite-passes ===

## User Acceptance

- None.

## Guardrails

- Keep the suite offline and stub fetch downloads.
- Run the suite from the application root through the POSIX-compatible launcher.
