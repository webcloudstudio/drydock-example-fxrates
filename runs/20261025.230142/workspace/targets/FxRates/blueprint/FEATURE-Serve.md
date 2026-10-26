# FEATURE: Serve API

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Run the HTTP API on the requested local port until stopped. |
| Depends On  | FEATURE-CliFoundation.md, FEATURE-ApiFoundation.md |
| Provides    | fxrates serve |
| Consumes    | app_server.main:app |

## Workflow

- `fxrates serve` runs uvicorn in the foreground using `app_server.main:app`.
- Bind only to `127.0.0.1`.
- Use the supplied `--port` value; when omitted, use port `8000`.
- Run until stopped, and stop cleanly on SIGTERM.
- A non-integer `--port` is a usage error with exit code 2.

## Programmatic Acceptance

=== AC serve_default_port ===
Intent: The CLI accepts serve without an explicit port and returns a running server process.
Requires: executable=python3; scope=test

import subprocess

process = subprocess.Popen(
    ["./fxrates", "serve"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
try:
    assert process.poll() is None
finally:
    process.terminate()
    process.wait(timeout=10)
=== END AC serve_default_port ===

=== AC serve_requested_port ===
Intent: The CLI accepts an explicit integer port and starts the server process.
Requires: executable=python3; scope=test

import socket
import subprocess

with socket.socket() as sock:
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]

process = subprocess.Popen(
    ["./fxrates", "serve", "--port", str(port)],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
try:
    assert process.poll() is None
finally:
    process.terminate()
    process.wait(timeout=10)
=== END AC serve_requested_port ===

=== AC serve_bad_port ===
Intent: A non-integer port is rejected as a usage error.
Requires: executable=python3; scope=test

import subprocess

result = subprocess.run(
    ["./fxrates", "serve", "--port", "notaport"],
    capture_output=True,
    text=True,
)
assert result.returncode == 2
=== END AC serve_bad_port ===

## User Acceptance

- None.

## Guardrails

- Bind the service to `127.0.0.1`.
- Keep the server in the foreground and stop cleanly on SIGTERM.
