# FEATURE: Command Help

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Each fxrates command accepts --help, prints usage and a one-line summary to standard output, and exits 0. |
| Depends On | FEATURE-InitCommand.md, FEATURE-LoadStore.md, FEATURE-Fetch.md, FEATURE-ServeHealth.md |
| Provides | fxrates --help |
| Consumes | fxrates init, fxrates load, fxrates fetch, fxrates serve |

## Purpose

Document every command's usage from the command line itself.

## Behavior

- `fxrates <command> --help` for `init`, `load`, `fetch`, and `serve` prints a usage line and a one-line summary to standard output and exits 0.
- Help is handled before the database is opened or a socket is bound, and before argument-count validation, so `load --help` needs no file argument.
- Nothing is written to standard error.

## Programmatic Acceptance

=== AC help-per-command ===
Intent: Each of the four commands exits 0 with non-empty standard output and empty standard error when given --help, including load without its file argument.
Requires: executable=python3; scope=test

from cli.testing import cli_runner

for command in ["init", "load", "fetch", "serve"]:
    code, out, err = cli_runner(command, "--help")
    assert code == 0, command
    assert out.strip() != "", command
    assert err == "", command
    assert command in out, command
=== END AC help-per-command ===

=== AC help-has-usage-and-summary ===
Intent: Help output has at least two non-blank lines: a usage line and a one-line summary.
Requires: executable=python3; scope=test

from cli.testing import cli_runner

for command in ["init", "load", "fetch", "serve"]:
    code, out, err = cli_runner(command, "--help")
    assert code == 0, command
    lines = [line for line in out.splitlines() if line.strip()]
    assert len(lines) >= 2, command
=== END AC help-has-usage-and-summary ===

=== AC help-does-not-touch-rates ===
Intent: init --help must not reset the store: a seeded rate is still there afterwards.
Requires: executable=python3; scope=test

from persistence.testing import db_session
from cli.testing import cli_runner

d = "2999-09-01"
c = "ZZA"
text = "6.5"

with db_session() as db:
    db.rates.replace_rate(date=d, currency=c, rate=text)
    code, out, err = cli_runner("init", "--help")
    assert code == 0
    rows = db.rates.list_currency_history(currency=c, start_date=d, end_date=d)
    assert [r.rate for r in rows] == [text]
=== END AC help-does-not-touch-rates ===

## User Acceptance

- None.

## Guardrails

- `--help` never opens the database or binds a socket.
- Diagnostics, if any, go to standard error and are never compared.
