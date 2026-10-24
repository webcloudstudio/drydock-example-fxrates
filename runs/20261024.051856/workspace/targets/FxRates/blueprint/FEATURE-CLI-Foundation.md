# FEATURE: CLI Foundation

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Establishes the `fxrates` command entry point and in-process runner contract. |
| Depends On  | ARCHITECTURE.md |
| Provides    | `./fxrates` entry point, `cli.main`, `cli.testing.cli_runner` |

## Purpose

The root executable dispatches commands through `cli.main(argv: list[str] | None) -> int`. Tests call the same implementation through `cli.testing.cli_runner(*args)`, which returns `(exit_code, stdout, stderr)` without spawning a process.

## Programmatic Acceptance

=== AC cli-main ===
Intent: The CLI exposes its documented callable entry point.

from cli import main

assert callable(main)
assert isinstance(main([]), int)
=== END AC cli-main ===

=== AC cli-runner ===
Intent: The in-process CLI runner returns an exit code and captured output streams.

from cli.testing import cli_runner

result = cli_runner()
assert isinstance(result, tuple)
assert len(result) == 3
assert isinstance(result[0], int)
assert isinstance(result[1], str)
assert isinstance(result[2], str)
=== END AC cli-runner ===

## User Acceptance

- None.

## Guardrails

- The root executable is named `fxrates` and is invoked as `./fxrates <command>`.
- CLI diagnostics use standard error.
