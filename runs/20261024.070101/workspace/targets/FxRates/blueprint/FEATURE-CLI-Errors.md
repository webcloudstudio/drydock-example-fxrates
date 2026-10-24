# FEATURE: CLI Errors

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines exit statuses and diagnostic behavior for command-line usage and operational failures. |
| Depends On  | FEATURE-CLI-Init.md, FEATURE-CLI-Load.md, FEATURE-CLI-Fetch.md, FEATURE-CLI-Serve.md |
| Provides    | CLI usage and operational error responses |
| Consumes     | fxrates init, fxrates load, fxrates fetch, fxrates serve |

## Behavior

The executable returns exit code 0 on success. Unknown commands, wrong argument counts, and a non-integer `--port` return exit code 2. Unreadable load files and fetch download failures return exit code 1. A failing command writes no standard output and exactly one diagnostic line to standard error. Diagnostic wording is concise and is not part of the response contract.

## Programmatic Acceptance

=== AC cli-usage-errors ===
Intent: Unknown commands, missing load arguments, and a non-integer server port return the usage exit status.

from cli.testing import cli_runner

assert cli_runner("frobnicate")[0] == 2
assert cli_runner("load")[0] == 2
assert cli_runner("serve", "--port", "notaport")[0] == 2
=== END AC cli-usage-errors ===

=== AC cli-operational-error ===
Intent: An unreadable input file returns the operational failure exit status.

from cli.testing import cli_runner

assert cli_runner("load", "sources/no-such-file.csv")[0] == 1
=== END AC cli-operational-error ===

## User Acceptance

- None.

## Guardrails

- Failures produce no standard output.
- Write one diagnostic line to standard error on failure.
- Do not make diagnostic wording part of the contract.
