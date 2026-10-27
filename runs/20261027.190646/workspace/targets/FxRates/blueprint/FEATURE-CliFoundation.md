# FEATURE: CLI Foundation

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | The cli package, command dispatcher, exit-code mapping and the fxrates executable. |
| Depends On | ARCHITECTURE.md, DATABASE.md |
| Provides | cli.main, cli.testing.cli_runner, fxrates |
| Consumes | config.database_path |

## Purpose

Provide the command-line entry point every command story plugs into without editing shared files.

## Interface

| Symbol | Contract |
|--------|----------|
| `cli.main(argv: list[str] \| None = None) -> int` | Dispatches `argv` (default `sys.argv[1:]`) and returns the exit code. |
| `cli.testing.cli_runner(*args) -> (code, stdout, stderr)` | Calls `main` in process with output captured. |
| `cli.errors` | `OperationalError` (`exit_code` 1), `UsageError` (2), `RejectedFile` (3); each subclasses `Exception`. |
| `cli.dispatch.execute(handler, args) -> int` | Calls `handler(args)`; returns its integer result, or maps a raised error to its `exit_code`, writing one diagnostic line to stderr and nothing to stdout. |
| `cli.commands.<name>.run(args) -> int` | Handler contract. The dispatcher imports the module for the first argument and calls `run` with the remaining arguments, so command stories add modules only. A command whose module cannot be imported is a `UsageError`. |
| `fxrates` | Executable at the application root: activates `.venv` when present and calls `cli.main`, exiting with its result. |

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC cli-runner-interface ===
Intent: cli_runner returns an (int, str, str) tuple without spawning a process, and a failing command writes nothing to standard output.
Requires: executable=python3; scope=test

import cli.commands
from cli import main
from cli.testing import cli_runner

name = "zzprobe-unknown-command"
result = cli_runner(name)
assert isinstance(result, tuple) and len(result) == 3
code, out, err = result
assert isinstance(code, int)
assert isinstance(out, str) and isinstance(err, str)
assert code != 0
assert out == ""
assert isinstance(main([name]), int)
=== END AC cli-runner-interface ===

=== AC dispatch-exit-codes ===
Intent: execute maps a clean handler to its result and each error class to exit codes 1, 2 and 3, with empty stdout and a single stderr line.
Requires: executable=python3; scope=test

import contextlib
import io

from cli.dispatch import execute
from cli.errors import OperationalError, RejectedFile, UsageError

assert OperationalError.exit_code == 1
assert UsageError.exit_code == 2
assert RejectedFile.exit_code == 3


def raiser(exc):
    def handler(args):
        raise exc
    return handler


def run(handler):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = execute(handler, [])
    return code, out.getvalue(), err.getvalue()


code, out, err = run(lambda args: 0)
assert code == 0
assert out == ""

for cls in (OperationalError, UsageError, RejectedFile):
    code, out, err = run(raiser(cls("probe failure")))
    assert code == cls.exit_code
    assert out == ""
    assert len(err.strip().splitlines()) == 1
=== END AC dispatch-exit-codes ===

=== AC fxrates-executable ===
Intent: The fxrates file exists at the application root, is executable and begins with an interpreter line.
Requires: executable=python3; scope=test

import os
from pathlib import Path

path = Path("fxrates")
assert path.is_file()
assert os.access(path, os.X_OK)
assert path.read_text(encoding="utf-8").startswith("#!")
=== END AC fxrates-executable ===

## User Acceptance

- None.

## Guardrails

- A failing command writes nothing to standard output and exactly one diagnostic line to standard error.
- Command stories add modules under `cli/commands/`; they do not edit the dispatcher.
- The CLI never imports a database driver.
