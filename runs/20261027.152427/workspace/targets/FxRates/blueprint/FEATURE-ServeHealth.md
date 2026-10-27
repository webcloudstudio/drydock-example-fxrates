# FEATURE: Serve Health

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | `fxrates serve` runs the FastAPI service on 127.0.0.1 and answers health, OpenAPI, and docs requests. |
| Depends On | FEATURE-WebFoundation.md, FEATURE-CliUsageErrors.md, FEATURE-DatabaseSelection.md |
| Provides | fxrates serve, GET /health, GET /openapi.json, GET /docs |
| Consumes | app_server.create_app, cli.main |

## Purpose

Start the HTTP API in the foreground and prove it is alive.

## Trigger

`./fxrates serve [--port <n>]`. Port validation (integer, 1 to 65535, otherwise exit 2) is owned by
the usage-error story and runs before any socket is bound.

## Sequence

1. Register the `serve` handler with the dispatcher.
2. Run uvicorn on `app_server.main:app` bound to `127.0.0.1` at the port, default `8000`, in the
   foreground. Nothing is required on standard output.
3. On SIGTERM stop cleanly and exit 0.
4. If the port is already bound, exit 1 with one stderr line and answer no requests.

## Routes

| Route | Status | Body |
|-------|--------|------|
| `GET /health` | 200 | `{"status": "ok"}` |
| `GET /openapi.json` | 200 | the FastAPI OpenAPI description |
| `GET /docs` | 200 | the interactive reference |

The OpenAPI and docs endpoints stay enabled. `/health` does not touch the database.

## Database Interface

- None — persistence is owned by DATABASE.md and `/health` reaches no store.

## Programmatic Acceptance

=== AC serve-health-route ===
Intent: The application answers GET /health with status 200 and the exact status body, and its OpenAPI description and interactive docs are served with status 200.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
response = client.get("/health")
assert response.status_code == 200
assert response.json() == {"status": "ok"}

spec = client.get("/openapi.json")
assert spec.status_code == 200
assert "/health" in spec.json()["paths"]

docs = client.get("/docs")
assert docs.status_code == 200
=== END AC serve-health-route ===

=== AC serve-live-sigterm ===
Intent: The serve command listens on 127.0.0.1 at the requested port, answers /health within a bounded wait, and exits 0 when it receives SIGTERM.
Requires: executable=python3; scope=test
Requires: python-package=uvicorn; scope=test

import json
import os
import signal
import socket
import subprocess
import tempfile
import time
import urllib.request

s = socket.socket()
s.bind(("127.0.0.1", 0))
port = s.getsockname()[1]
s.close()

work = tempfile.mkdtemp()
env = {**os.environ, "DATABASE_URL": os.path.join(work, "serve.db")}
proc = subprocess.Popen(
    [os.path.abspath("fxrates"), "serve", "--port", str(port)],
    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
)
try:
    deadline = time.time() + 30
    body = None
    while time.time() < deadline:
        if proc.poll() is not None:
            break
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2) as r:
                assert r.status == 200
                body = json.loads(r.read())
            break
        except OSError:
            time.sleep(0.25)
    assert proc.poll() is None, "server exited before answering /health"
    assert body == {"status": "ok"}
    proc.send_signal(signal.SIGTERM)
    rc = proc.wait(timeout=20)
    assert rc == 0
finally:
    if proc.poll() is None:
        proc.kill()
    out, err = proc.communicate()
    print(out.decode("utf-8", "replace"))
    print(err.decode("utf-8", "replace"))
=== END AC serve-live-sigterm ===

=== AC serve-port-in-use ===
Intent: When the requested port is already bound, serve exits 1 with empty stdout and one stderr line instead of serving.
Requires: executable=python3; scope=test
Requires: python-package=uvicorn; scope=test

import os
import socket
import subprocess
import tempfile

blocker = socket.socket()
blocker.bind(("127.0.0.1", 0))
blocker.listen(1)
port = blocker.getsockname()[1]

work = tempfile.mkdtemp()
env = {**os.environ, "DATABASE_URL": os.path.join(work, "busy.db")}
proc = subprocess.Popen(
    [os.path.abspath("fxrates"), "serve", "--port", str(port)],
    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
)
try:
    out, err = proc.communicate(timeout=30)
    print(out.decode("utf-8", "replace"))
    print(err.decode("utf-8", "replace"))
    assert proc.returncode == 1
    assert out == b""
    assert len(err.decode("utf-8", "replace").strip().splitlines()) == 1
finally:
    if proc.poll() is None:
        proc.kill()
        proc.communicate()
    blocker.close()
=== END AC serve-port-in-use ===

## User Acceptance

- None.

## Guardrails

- The server binds 127.0.0.1 only and has no authentication; it serves public ECB reference rates.
- Standard error is diagnostics only and is never compared.
- `serve` stops cleanly on SIGTERM and exits 0.
