# FEATURE: CLI Foundation

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Establishes the root fxrates executable and its command-line dispatch package. |
| Depends On  | ARCHITECTURE.md |
| Provides    | ./fxrates entry point, CLI main(argv) |
| Consumes    | — |

## Purpose

Provide the root `./fxrates` executable and the `cli` package entry point. `cli.main(argv: list[str] | None = None) -> int` dispatches the planned `init`, `load`, `fetch`, and `serve` commands. It returns the command exit status. Usage errors return 2; operational errors return 1; rejected input files return 3. Diagnostics are written to standard error.

## Programmatic Acceptance

=== AC cli-entrypoint ===
Intent: The published CLI entry point is callable and returns a usage error for an unknown command.

from cli import main

assert callable(main)
assert main(["frobnicate"]) == 2
=== END AC cli-entrypoint ===

=== AC cli-runner ===
Intent: The published CLI runner returns an exit code and captured output streams for a usage error.

from cli.testing import cli_runner

result = cli_runner("load")
assert isinstance(result, tuple)
assert len(result) == 3
assert result[0] == 2
=== END AC cli-runner ===

## User Acceptance

- None.

## Guardrails

- Provide an executable named `fxrates` at the application root.
- Keep diagnostics on standard error.
- Use the published `cli.main(argv)` and `cli.testing.cli_runner` interfaces.
