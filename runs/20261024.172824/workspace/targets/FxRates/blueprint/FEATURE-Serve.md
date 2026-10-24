# FEATURE: Serve API

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Runs the FastAPI rates service on the requested local port. |
| Depends On  | ARCHITECTURE.md |
| Provides    | fxrates serve |
| Consumes    | app_server.main:create_app |

## Purpose

`./fxrates serve [--port <n>]` runs the HTTP API in the foreground on `127.0.0.1`. The default port is `8000`. The process stays running until stopped and shuts down cleanly on SIGTERM.

## Workflow

Create and serve the application through the shared FastAPI application factory. Bind only to the loopback address and pass the selected port to uvicorn. If no port is supplied, use `8000`.

## Programmatic Acceptance

=== AC serve-uses-port-and-stops ===
Intent: The serve command starts the API on the requested loopback port and exits after SIGTERM.

import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

port_socket = socket.socket()
port_socket.bind(("127.0.0.1", 0))
port = port_socket.getsockname()[1]
port_socket.close()

process = subprocess.Popen(
    ["./fxrates", "serve", "--port", str(port)],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
try:
    deadline = time.monotonic() + 15
    response = None
    while time.monotonic() < deadline:
        try:
            response = urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=1)
            break
        except (OSError, urllib.error.URLError):
            time.sleep(0.1)
    assert response is not None
    assert response.status == 200
finally:
    process.terminate()
    assert process.wait(timeout=10) == 0
=== END AC serve-uses-port-and-stops ===

## User Acceptance

- None.

## Guardrails

- Bind to `127.0.0.1`, not a public interface.
- Keep the server in the foreground.
- Honor the supplied port and default to `8000`.
- Stop cleanly on SIGTERM.
