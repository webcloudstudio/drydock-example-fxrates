# FEATURE: CLI Usage Errors

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Argument validation that reports usage errors with exit 2, empty stdout, and one stderr line. |
| Depends On | FEATURE-CliFoundation.md |
| Provides | fxrates usage validation |
| Consumes | cli.main |

## Purpose

Reject malformed invocations before any handler, database, or socket is touched.

## Behavior

`cli/usage.py` provides `UsageError` and `validate(argv: list[str]) -> None`; `cli.main` calls it
before dispatch and, on `UsageError`, writes one line to standard error, nothing to standard output,
and returns `2`.

| Command | Arguments |
|---------|-----------|
| `init` | none |
| `load` | exactly one (the CSV path) |
| `fetch` | none |
| `serve` | optional `--port <n>`; `n` an integer from 1 to 65535 |

- No command, or a command in neither this table nor the handler registry, is a usage error.
- A wrong argument count, a `--port` without a value, a non-integer `--port`, and a `--port`
  outside 1 to 65535 are usage errors.
- A command registered but absent from the table is not arity-checked.
- A lone `--help` after a known command is passed through to its handler.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC usage-rejected-invocations ===
Intent: Each malformed invocation exits 2 with empty stdout and exactly one stderr line.
Requires: executable=python3; scope=test

from cli.testing import cli_runner

cases = [
    [],
    ["frobnicate"],
    ["load"],
    ["load", "a.csv", "b.csv"],
    ["init", "extra"],
    ["fetch", "extra"],
    ["serve", "--port", "notaport"],
    ["serve", "--port"],
    ["serve", "--port", "0"],
    ["serve", "--port", "65536"],
    ["serve", "--port", "-1"],
]
for argv in cases:
    code, out, err = cli_runner(*argv)
    assert code == 2, argv
    assert out == "", argv
    assert len(err.strip().splitlines()) == 1, argv
=== END AC usage-rejected-invocations ===

=== AC usage-valid-ports-pass-validation ===
Intent: Boundary ports and no port are valid, and validation raises UsageError only for invalid input.
Requires: executable=python3; scope=test

from cli.usage import UsageError, validate

for argv in (["serve"], ["serve", "--port", "1"], ["serve", "--port", "65535"],
             ["serve", "--port", "8000"], ["init"], ["load", "x.csv"], ["fetch"]):
    validate(argv)

bad = ["serve", "--port", "65536"]
try:
    validate(bad)
except UsageError:
    pass
else:
    raise AssertionError("expected UsageError")
=== END AC usage-valid-ports-pass-validation ===

=== AC usage-executable-exit-2 ===
Intent: The fxrates executable itself exits 2 with empty stdout for an unknown command.
Requires: executable=python3; scope=test

import subprocess

result = subprocess.run(["./fxrates", "frobnicate"], capture_output=True, text=True,
                        stdin=subprocess.DEVNULL)
print(result.stdout)
print(result.stderr)
assert result.returncode == 2
assert result.stdout == ""
=== END AC usage-executable-exit-2 ===

## User Acceptance

- None.

## Guardrails

- Validation never opens a database or binds a socket.
- Error message wording is not part of the contract; only exit status, empty stdout, and a single stderr line are.
