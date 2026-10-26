# FEATURE: CLI Foundation

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Provides the callable command-line entry point and root executable foundation. |
| Depends On  | ARCHITECTURE.md |
| Provides    | `cli.main(argv: list[str] | None) -> int`, `./fxrates` |
| Consumes    |  |

## Purpose

The `cli` package exposes `main(argv: list[str] | None = None) -> int`, and the executable at the application root delegates to it. Feature stories add the supported subcommands.

## Programmatic Acceptance

=== AC cli_entry_point ===
Intent: The CLI foundation exposes a callable entry point returning an integer status.

from cli import main

result = main(["__foundation_probe__"])
assert isinstance(result, int)
=== END AC cli_entry_point ===

=== AC cli_runner_contract ===
Intent: The published CLI runner returns an integer exit code and captured output strings.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("__foundation_probe__")
assert isinstance(code, int)
assert isinstance(stdout, str)
assert isinstance(stderr, str)
=== END AC cli_runner_contract ===

## User Acceptance

- None.

## Guardrails

- The root executable is named `fxrates`.
- Diagnostics are written to standard error.
- Command implementations use the declared persistence boundary when accessing stored rates.
