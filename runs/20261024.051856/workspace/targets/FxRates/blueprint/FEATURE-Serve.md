# FEATURE: Serve HTTP API

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Runs the FastAPI service on localhost until it is stopped. |
| Depends On  | FEATURE-CLI-Foundation.md, FEATURE-API-Foundation.md |
| Provides    | fxrates serve |
| Consumes    | app_server.main:create_app |

## Purpose

The `fxrates serve` command starts uvicorn in the foreground, bound only to `127.0.0.1`. It accepts an optional integer port and defaults to port `8000`. The process stops cleanly on SIGTERM.

## Trigger and behavior

Running `./fxrates serve` starts the service on `127.0.0.1:8000`. Running `./fxrates serve --port <n>` starts it on `127.0.0.1:<n>`. The API application is supplied by `app_server.main:create_app`.

## Programmatic Acceptance

=== AC serve-command-entry ===
Intent: The CLI exposes the serve command.

from cli import main

assert callable(main)
=== END AC serve-command-entry ===

=== AC serve-app-factory ===
Intent: The server command's application factory is available.

from app_server.main import create_app

assert callable(create_app)
=== END AC serve-app-factory ===

## User Acceptance

- None.

## Guardrails

- Bind to `127.0.0.1`; use port `8000` when none is supplied.
- Run in the foreground and stop cleanly on SIGTERM.
