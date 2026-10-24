# FEATURE: CLI Foundation

| Field | Value |
|-------|-------|
| Version | 20261024 V1 |
| Description | Establishes the root fxrates executable and command dispatch. |
| Depends On | ARCHITECTURE.md, DATABASE.md |
| Provides | fxrates executable, fxrates init, fxrates load, fxrates fetch, fxrates serve |
| Consumes | rates repository operations |

## Purpose

Provide the executable `./fxrates` at the application root and dispatch the four supported commands: `init`, `load`, `fetch`, and `serve`.

## Command Contract

- `init` takes no arguments, initializes the rates table, and returns exit code 0 on success.
- `load` takes one CSV path.
- `fetch` takes no arguments.
- `serve` accepts optional `--port <n>` and defaults to port 8000. It serves on `127.0.0.1` until stopped.
- Success output and command-specific behavior are defined by the implementing feature specifications.
- Usage errors return 2. A non-integer port is a usage error.
- A failing command writes no stdout and one diagnostic line to stderr.

## Programmatic Acceptance

=== AC cli-dispatch ===
Intent: The CLI foundation exposes a callable dispatcher and handles unknown commands with the usage exit status.

from cli import main

assert callable(main)
assert main(["frobnicate"]) == 2
=== END AC cli-dispatch ===

=== AC cli-test-helper ===
Intent: The CLI testing helper returns an exit code and captured output streams.

from cli.testing import cli_runner

result = cli_runner("frobnicate")
assert isinstance(result, tuple)
assert len(result) == 3
assert result[0] == 2
assert isinstance(result[1], str)
assert isinstance(result[2], str)
=== END AC cli-test-helper ===

## User Acceptance

- None.

## Guardrails

- Keep diagnostics on standard error.
- Do not invent command behavior beyond the source contract.
- The executable must be runnable as `./fxrates <command>`.
