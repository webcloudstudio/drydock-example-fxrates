# FEATURE: Usage Errors

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Command-line argument validation that reports usage errors with exit status 2 before any handler runs. |
| Depends On | FEATURE-CliFoundation.md |
| Provides | fxrates usage validation |
| Consumes | cli.main |

## Purpose

Reject malformed invocations uniformly and hand valid ones to handlers as parsed values.

## Behavior

`cli.usage.parse(argv) -> (name, args)` validates before any handler runs and raises `cli.errors.UsageError` on a violation. `main` calls it first, so a usage error exits 2 with one stderr line and empty stdout.

| Command | Accepted arguments | `args` handed to `run` |
|---------|--------------------|------------------------|
| `init` | none | `[]` |
| `fetch` | none | `[]` |
| `load` | exactly one path | `[path]` |
| `serve` | optional `--port <n>`, `n` an integer, default 8000 | `[port]` with `port` an `int` |

No command, an unknown command, the wrong argument count, an unknown option, or a `--port` value that is missing or not an integer is a usage error.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC usage-errors-exit-2 ===
Intent: Every malformed invocation exits 2 with empty stdout and a single stderr line, before any store is touched.
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
]
for argv in cases:
    code, out, err = cli_runner(*argv)
    assert code == 2, argv
    assert out == "", argv
    assert len(err.strip().splitlines()) == 1, argv
=== END AC usage-errors-exit-2 ===

=== AC parse-valid-arguments ===
Intent: parse hands valid arguments on as parsed values, with the serve port an integer defaulting to 8000.
Requires: executable=python3; scope=test

from cli.usage import parse

port = 9123
path = "rates.csv"

assert parse(["init"]) == ("init", [])
assert parse(["fetch"]) == ("fetch", [])
assert parse(["load", path]) == ("load", [path])
assert parse(["serve", "--port", str(port)]) == ("serve", [port])
assert parse(["serve"]) == ("serve", [8000])
=== END AC parse-valid-arguments ===

=== AC parse-raises-usage-error ===
Intent: parse signals each violation with UsageError, whose exit code is 2.
Requires: executable=python3; scope=test

from cli.errors import UsageError
from cli.usage import parse

bad = [
    [],
    ["frobnicate"],
    ["load"],
    ["load", "a", "b"],
    ["serve", "--port", "x1"],
]
for argv in bad:
    try:
        parse(argv)
    except UsageError as exc:
        assert exc.exit_code == 2
    else:
        raise AssertionError(argv)
=== END AC parse-raises-usage-error ===

## User Acceptance

- None.

## Guardrails

- A usage error writes nothing to standard output and exactly one diagnostic line to standard error.
- Validation runs before any handler, so a usage error never opens or changes the store.
