# FEATURE: CLI Serve

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Runs the local JSON API in the foreground on the requested port or the default port. |
| Depends On  | FEATURE-CLI-Foundation.md, FEATURE-API-Foundation.md, FEATURE-API-Health.md |
| Provides    | fxrates serve |
| Consumes     | app_server.main:app |

## Purpose

Run the FastAPI application with uvicorn bound to `127.0.0.1`. Accept an optional integer port and default to port 8000. Keep serving until stopped and exit cleanly on SIGTERM.

## Programmatic Acceptance

Requires: python-package=httpx; scope=test

=== AC serve-requested-port ===
Intent: The serve command starts the health route on an available requested local port and stops on SIGTERM.

import socket
import subprocess
import time
import httpx

with socket.socket() as sock:
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]

process = subprocess.Popen(["./fxrates", "serve", "--port", str(port)])
try:
    response = None
    for _ in range(100):
        if process.poll() is not None:
            break
        try:
            response = httpx.get(f"http://127.0.0.1:{port}/health", timeout=0.5)
            break
        except httpx.HTTPError:
            time.sleep(0.05)
    assert response is not None
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
finally:
    process.terminate()
    assert process.wait(timeout=10) == 0
=== END AC serve-requested-port ===

=== AC serve-default-port-contract ===
Intent: The command accepts the serve invocation without a port argument.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("serve", "--help")
assert code == 0
=== END AC serve-default-port-contract ===

## User Acceptance

- None.

## Guardrails

- Bind only to `127.0.0.1`.
- The server runs in the foreground and stops cleanly on SIGTERM.
- The default port is 8000.
