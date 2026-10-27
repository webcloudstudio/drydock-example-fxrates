# FEATURE: CLI Foundation

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Establishes the root executable and the published in-process CLI entry point. |
| Depends On  | ARCHITECTURE.md |

## Purpose

Provide the application-root executable `./fxrates`, the `cli.main(argv: list[str] | None = None) -> int` entry point, and the `cli.testing.cli_runner(*args)` helper. Feature stories own command behavior and its implementation.

## Interface

- `./fxrates <command>` invokes `cli.main`.
- `cli.testing.cli_runner(*args)` returns `(exit_code, stdout, stderr)` without spawning a process.
- Diagnostics are written to standard error.

## Programmatic Acceptance

=== AC cli-foundation-interfaces ===
Intent: The CLI entry point and in-process runner expose the published callable interfaces.
from cli import main
from cli.testing import cli_runner
import inspect

assert callable(main)
assert inspect.signature(main).parameters["argv"].default is None
result = cli_runner()
assert isinstance(result, tuple)
assert len(result) == 3
assert isinstance(result[0], int)
assert isinstance(result[1], str)
assert isinstance(result[2], str)
=== END AC cli-foundation-interfaces ===

## User Acceptance

- None.

## Guardrails

- Place an executable named `fxrates` at the application root.
- Keep command diagnostics on standard error.
- Command-specific behavior and error statuses are implemented by their owning stories.
