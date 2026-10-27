# FEATURE: Command Line Foundation

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | The cli package entry point, dispatcher, test runner, and the executable fxrates at the application root. |
| Depends On | ARCHITECTURE.md, DATABASE.md |
| Provides | fxrates, cli.main, cli.testing.cli_runner |

## Purpose

Provide the shell every command story plugs into: `cli.main(argv) -> int`, a registry mapping a
command name to a handler, and the `fxrates` launcher. This story proves only the interface.

## Interface

```python
# cli/__init__.py
def main(argv: list[str] | None = None) -> int: ...
def register_command(name: str, handler: Callable[[list[str]], int]) -> None: ...

# cli/testing.py
def cli_runner(*args: str) -> tuple[int, str, str]: ...
```

- `main` dispatches `argv[0]` to the registered handler, passing the remaining arguments, and
  returns the handler's integer exit code. Diagnostics go to standard error.
- `register_command` is called by command stories at import time; registering a name again replaces
  the earlier handler.
- `cli_runner` calls `main` in-process and returns `(exit_code, stdout, stderr)`.
- `fxrates` is a POSIX sh script at the application root with the executable bit set. It activates
  `.venv` when present, runs `cli.main` with its arguments, and exits with the returned code.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC cli-main-returns-int ===
Intent: main returns an integer exit code and cli_runner reports it with captured streams.
Requires: executable=python3; scope=test

from cli import main
from cli.testing import cli_runner

code, out, err = cli_runner()
assert isinstance(code, int)
assert isinstance(out, str) and isinstance(err, str)
assert isinstance(main([]), int)
=== END AC cli-main-returns-int ===

=== AC cli-dispatch-registered ===
Intent: A registered handler receives the remaining arguments and its exit code is main's return value.
Requires: executable=python3; scope=test

from cli import main, register_command

seen = []
wanted = 7
args = ["alpha", "beta"]

def handler(rest):
    seen.append(list(rest))
    return wanted

register_command("zz-probe", handler)
assert main(["zz-probe", *args]) == wanted
assert seen == [args]
=== END AC cli-dispatch-registered ===

=== AC cli-executable-runs ===
Intent: The fxrates launcher exists at the application root with the executable bit and runs to an integer exit status.
Requires: executable=python3; scope=test

import os
import subprocess

assert os.path.isfile("fxrates")
assert os.access("fxrates", os.X_OK)
result = subprocess.run(["./fxrates"], capture_output=True, text=True, stdin=subprocess.DEVNULL)
print(result.stdout)
print(result.stderr)
assert result.returncode not in (126, 127)
=== END AC cli-executable-runs ===

## User Acceptance

- None.

## Guardrails

- The executable is invoked as `./fxrates <command>`; it contains no command logic of its own.
- Diagnostics go to standard error and are never compared.
- No database driver is imported in the `cli` package.
