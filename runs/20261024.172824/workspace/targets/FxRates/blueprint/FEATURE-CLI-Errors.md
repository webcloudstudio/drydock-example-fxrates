# FEATURE: CLI Errors and Test Runner

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines CLI failure behavior and the project test launcher. |
| Depends On  | ARCHITECTURE.md |
| Provides    | fxrates usage and failure responses, bin/test.sh |
| Consumes    | fxrates init, fxrates load, fxrates fetch, fxrates serve |

## Purpose

CLI usage errors, rejected files, and operational failures use the exit statuses declared for each condition. Every failed command writes no standard output and one diagnostic line to standard error. `bin/test.sh` runs the project pytest suite from the application root.

## CLI Failure Contract

- Exit `0`: success.
- Exit `1`: operational failure, including unreadable input or failed fetch download.
- Exit `2`: unknown command, wrong argument count, or non-integer `--port`.
- Exit `3`: rejected CSV file.
- Failure output is empty on standard output and one line on standard error.

## Test Launcher

Provide an executable POSIX-compatible `bin/test.sh` that runs pytest from the application root and exits zero only when every automated test passes.

## Programmatic Acceptance

=== AC cli-usage-error-status ===
Intent: Unknown commands and missing command arguments return the usage exit status.

from cli.testing import cli_runner

assert cli_runner("unknown")[0] == 2
assert cli_runner("load")[0] == 2
=== END AC cli-usage-error-status ===

=== AC cli-operational-error-status ===
Intent: An unreadable input file returns the operational failure status.

from cli.testing import cli_runner

assert cli_runner("load", "missing-file.csv")[0] == 1
=== END AC cli-operational-error-status ===

=== AC test-launcher ===
Intent: The project test launcher exits successfully when the project's tests pass.

import subprocess

result = subprocess.run(["sh", "bin/test.sh"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
assert result.returncode == 0
=== END AC test-launcher ===

## User Acceptance

- None.

## Guardrails

- Keep diagnostics on standard error; do not emit standard output on failure.
- Preserve the specified exit codes.
- The test launcher must use POSIX-compatible shell syntax.
