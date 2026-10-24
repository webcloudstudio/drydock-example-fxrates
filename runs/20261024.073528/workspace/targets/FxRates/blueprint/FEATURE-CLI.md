# FEATURE: CLI

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines the root executable commands, help, arguments, and CLI error behavior. |
| Depends On  | ARCHITECTURE.md, DATABASE.md, FEATURE-Rate-Loading.md, FEATURE-Rate-Fetch.md |
| Provides    | fxrates init, fxrates load, fxrates fetch, fxrates serve |
| Consumes    | cli.main, rates.delete |

## Purpose

Provide the executable `./fxrates` at the application root with the commands `init`, `load`, `fetch`, and `serve`. The module callable `cli.main(argv: list[str] | None = None) -> int` is the implementation entry point; the executable delegates to it.

## Commands

| Command | Behavior | Success output |
|---------|----------|----------------|
| `init` | Drop the existing `rates` table and recreate it empty through the persistence boundary. | Empty |
| `load <csv>` | Delegate to the shared loader. | Loader output |
| `fetch` | Delegate to the archive fetcher. | Loader output |
| `serve [--port <n>]` | Run uvicorn on `127.0.0.1`, default port 8000, until stopped. | No output required |

Each command has usable help that documents its supported arguments. No command argument or an unknown command is a usage error. Unknown command, wrong argument count, and non-integer `--port` return exit code 2. Operational failures return 1; rejected CSV returns 3. Failures write no stdout and one diagnostic line to stderr. `serve` stops cleanly on SIGTERM.

## Programmatic Acceptance

=== AC cli-callable ===
Intent: The public CLI entry point returns a usage status for an unknown command.

from cli import main

assert main(["unknown-command"]) == 2
=== END AC cli-callable ===

=== AC cli-load-dispatch ===
Intent: The CLI exposes the load command and dispatches a valid staged file successfully.

from cli.testing import cli_runner

code, _, _ = cli_runner("load", "sources/eurofxref-hist_2025-01.csv")
assert code == 0
=== END AC cli-load-dispatch ===

=== AC cli-fetch-dispatch ===
Intent: The CLI exposes fetch and uses a stubbed archive download successfully.

from unittest.mock import patch
from cli.testing import cli_runner

with patch("rate_fetch.download_archive", return_value=b"Date,USD,\n2099-01-06,1.25,\n"):
    code, _, _ = cli_runner("fetch")
assert code == 0
=== END AC cli-fetch-dispatch ===

=== AC cli-serve-entry ===
Intent: The CLI's serve command accepts an integer port and returns through the application server callable.

from unittest.mock import patch
from cli import main

with patch("uvicorn.run", return_value=None) as run:
    assert main(["serve", "--port", "8123"]) == 0
    assert run.called
=== END AC cli-serve-entry ===

=== AC cli-help ===
Intent: The command line entry point provides help without reporting an error.

from cli import main

assert main(["--help"]) == 0
assert main(["load", "--help"]) == 0
assert main(["fetch", "--help"]) == 0
assert main(["serve", "--help"]) == 0
=== END AC cli-help ===

=== AC cli-usage-errors ===
Intent: Invalid command arguments return the documented usage status.

from cli import main

assert main([]) == 2
assert main(["unknown-command"]) == 2
assert main(["load"]) == 2
assert main(["serve", "--port", "notaport"]) == 2
=== END AC cli-usage-errors ===

## User Acceptance

- None.

## Guardrails

- The root `fxrates` executable must be executable and delegate to `cli.main`.
- Initialization must use the declared persistence boundary to drop and recreate the rates table.
- Command tests and fetch tests must not make network connections.
- Keep failures off stdout and send one diagnostic line to stderr.
- `cli.main` may not manipulate the database directly; it calls declared operations or feature interfaces.

## Database Interface

- `FEATURE-RATE-003` — write: rates.delete - supplies: `date`, `currency` - returns: `date`, `currency`
