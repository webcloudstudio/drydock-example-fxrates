# FEATURE: CLI Foundation

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Provides the executable and callable entry points for the FxRates command line. |
| Depends On  | ARCHITECTURE.md |
| Provides    | ./fxrates, cli.main, cli.testing:cli_runner |

## Purpose

Provide the root-level executable and a callable command entry point so commands can be exercised in-process by the application and its tests.

## Interfaces

- `cli.main(argv: list[str] | None = None) -> int`
- `cli.testing.cli_runner(*args: str) -> tuple[int, str, str]`, returning exit code, standard output, and standard error without spawning a process.
- `./fxrates <command>` invokes the CLI entry point.

## Programmatic Acceptance

=== AC cli-entry-points ===
Intent: The CLI entry point and in-process runner are callable.

from cli import main
from cli.testing import cli_runner

assert callable(main)
assert callable(cli_runner)
result = cli_runner()
assert isinstance(result, tuple)
assert len(result) == 3
=== END AC cli-entry-points ===

=== AC fxrates-executable ===
Intent: The application root contains an executable named fxrates.

from pathlib import Path
import os

executable = Path("fxrates")
assert executable.is_file()
assert os.access(executable, os.X_OK)
=== END AC fxrates-executable ===

## User Acceptance

- None.

## Guardrails

- Keep the executable named `fxrates` at the application root.
- The CLI runner returns `(exit_code, stdout, stderr)` without spawning a process.
- Command-specific behavior and exit codes belong to their respective CLI feature specifications.
