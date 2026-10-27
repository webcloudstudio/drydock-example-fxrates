# FEATURE: CLI Errors

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Defines command-line usage and operational error behavior for fxrates. |
| Depends On  | FEATURE-CLI.md |
| Provides    | CLI usage and error exit behavior |
| Consumes    | ./fxrates |

## Purpose

Give every command a consistent failure contract. Failed commands write no standard output and one diagnostic line to standard error.

## Behavior

- Unknown commands, incorrect argument counts, and a non-integer `serve --port` value exit with status 2.
- A file that cannot be read exits with status 1.
- A CSV rejected by the load validator exits with status 3.
- Keep failure messages on standard error; their wording is not part of the contract.

## Programmatic Acceptance

=== AC cli-usage-errors ===
Intent: Usage errors return status 2 and produce no standard output.

from cli.testing import cli_runner

for args in (("frobnicate",), ("load",), ("serve", "--port", "notaport")):
    code, stdout, stderr = cli_runner(*args)
    assert code == 2
    assert stdout == ""
    assert stderr
=== END AC cli-usage-errors ===

=== AC cli-operational-errors ===
Intent: File read failures return status 1 and rejected CSV files return status 3.

from cli.testing import cli_runner

missing_path = "sources/absent-for-cli-error-check.csv"
code, stdout, stderr = cli_runner("load", missing_path)
assert code == 1
assert stdout == ""
assert stderr

code, stdout, stderr = cli_runner("load", "sources/eurofxref-hist_bad.csv")
assert code == 3
assert stdout == ""
assert stderr
=== END AC cli-operational-errors ===

## User Acceptance

- None.

## Guardrails

- Keep diagnostics on standard error.
- Do not emit standard output for failed commands.
- Preserve the distinct exit statuses for usage, operational, and rejected-file failures.
