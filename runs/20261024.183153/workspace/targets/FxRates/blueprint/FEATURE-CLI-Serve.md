# FEATURE: CLI Serve

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Starts the FxRates HTTP service from the command line. |
| Depends On  | ARCHITECTURE.md, FEATURE-API-Health.md |
| Provides    | `fxrates serve` |
| Consumes    | application ASGI app |

## Purpose

Run the API on `127.0.0.1` in the foreground until stopped. `--port <n>` selects the port; when omitted, use port `8000`. Stop cleanly on SIGTERM.

## Workflow

1. Parse `serve` and its optional `--port` argument.
2. Run the application ASGI app with uvicorn bound to `127.0.0.1` and the selected port.
3. Keep the command in the foreground and exit cleanly after SIGTERM.

A non-integer port is a usage error with exit code `2`. The server writes no required standard output.

## Programmatic Acceptance

=== AC serve-health ===
Intent: The serve command starts the declared application and exposes its health route.

from app_server.main import create_app
from fastapi.testclient import TestClient

client = TestClient(create_app())
response = client.get("/health")
assert response.status_code == 200
=== END AC serve-health ===

=== AC serve-cli-usage ===
Intent: A non-integer port is rejected with the declared usage exit code.

from cli.testing import cli_runner

exit_code, stdout, stderr = cli_runner("serve", "--port", "notaport")
assert exit_code == 2
=== END AC serve-cli-usage ===

## User Acceptance

- None.

## Guardrails

- Bind only to `127.0.0.1`.
- Run in the foreground and stop cleanly on SIGTERM.
- Do not require standard output from the serving command.
