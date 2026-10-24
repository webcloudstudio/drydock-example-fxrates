# FEATURE: CLI Server

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Runs the JSON API on the requested local port until stopped. |
| Depends On  | ARCHITECTURE.md, FEATURE-API-Health-Stats.md |
| Provides    | fxrates serve |
| Consumes    | FastAPI application |

## Purpose

`fxrates serve [--port <n>]` runs uvicorn in the foreground, binding the API to `127.0.0.1` at the requested port, defaulting to 8000. It continues until stopped and handles SIGTERM cleanly. It does not require standard output.

## Programmatic Acceptance

=== AC serve-stops-on-sigterm ===
Intent: The serve command starts the local API and exits after receiving SIGTERM.

import signal
import socket
import subprocess
import time

with socket.socket() as sock:
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]

process = subprocess.Popen(
    ["./fxrates", "serve", "--port", str(port)],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
try:
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise AssertionError("serve exited before becoming available")
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                break
        except OSError:
            time.sleep(0.05)
    else:
        raise AssertionError("serve did not bind the requested port")
    process.send_signal(signal.SIGTERM)
    assert process.wait(timeout=5) == 0
finally:
    if process.poll() is None:
        process.terminate()
        process.wait(timeout=5)
=== END AC serve-stops-on-sigterm ===

## User Acceptance

- None.

## Guardrails

- Bind only to `127.0.0.1`.
- Default to port 8000 when `--port` is omitted.
- Keep the server in the foreground and stop cleanly on SIGTERM.
