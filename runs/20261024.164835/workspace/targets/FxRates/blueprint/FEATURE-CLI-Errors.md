# FEATURE: CLI Errors

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Reports command usage, operational, and rejected-file failures through exit codes and diagnostics. |
| Depends On  | FEATURE-CLI-Foundation.md, FEATURE-ECB-Init.md, FEATURE-ECB-Load.md, FEATURE-ECB-Fetch.md, FEATURE-CLI-Serve.md |
| Provides    | CLI exit codes and diagnostics |
| Consumes     | fxrates init, fxrates load, fxrates fetch, fxrates serve |

## Purpose

Apply the command-line exit contract across commands. Successful operations return zero. Operational failures return one, usage errors return two, and rejected history files return three. Any failing command writes no standard output and one diagnostic line to standard error.

## Programmatic Acceptance

=== AC cli-usage-errors ===
Intent: Missing and unknown commands and invalid command arguments return the usage exit status without standard output.

from cli.testing import cli_runner

for args in ((), ("frobnicate",), ("load",), ("serve", "--port", "notaport")):
    code, stdout, stderr = cli_runner(*args)
    assert code == 2
    assert stdout == ""
    assert len(stderr.splitlines()) == 1
=== END AC cli-usage-errors ===

=== AC cli-load-errors ===
Intent: A rejected file and an unreadable file return their distinct failure statuses without standard output.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("load", "sources/eurofxref-hist_bad.csv")
assert code == 3
assert stdout == ""
assert len(stderr.splitlines()) == 1

code, stdout, stderr = cli_runner("load", "sources/no-such-file.csv")
assert code == 1
assert stdout == ""
assert len(stderr.splitlines()) == 1
=== END AC cli-load-errors ===

=== AC cli-success-status ===
Intent: A successful initialization returns zero and no standard output.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("init")
assert code == 0
assert stdout == ""
=== END AC cli-success-status ===

## User Acceptance

- None.

## Guardrails

- Exit codes are 0 for success, 1 for operational failure, 2 for usage error, and 3 for rejected file.
- Failing commands write nothing to standard output and one diagnostic line to standard error.
- Diagnostics are not specified by message text.
