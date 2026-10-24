# FEATURE: CLI Serve

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Starts the JSON API server on localhost. |
| Depends On  | ARCHITECTURE.md, FEATURE-API-Overview.md, FEATURE-API-Rates.md, FEATURE-API-Convert.md, FEATURE-API-History.md |
| Provides    | fxrates serve |
| Consumes    | app_server.main:app |

## Purpose

`fxrates serve [--port <n>]` runs uvicorn in the foreground on `127.0.0.1`, using port 8000 by default, until stopped.

## Workflow

The command accepts an optional integer port. An invalid port argument is a usage error. The server binds only to `127.0.0.1`, serves the API application, and terminates cleanly on SIGTERM.

## Programmatic Acceptance

=== AC serve-invalid-port ===
Intent: A non-integer port is rejected as a usage error.

from cli.testing import cli_runner

code, out, _ = cli_runner("serve", "--port", "notaport")
assert code == 2
assert out == ""
=== END AC serve-invalid-port ===

=== AC serve-default-config ===
Intent: The serve command exposes its foreground server configuration for the default port and localhost binding.

from cli import server
config = server.serve_config([])
assert config.host == "127.0.0.1"
assert config.port == 8000
=== END AC serve-default-config ===

## User Acceptance

- None.

## Guardrails

- Bind the server to 127.0.0.1 only.
- Keep serving in the foreground and stop cleanly on SIGTERM.
