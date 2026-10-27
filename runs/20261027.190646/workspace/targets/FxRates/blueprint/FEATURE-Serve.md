# FEATURE: Serve

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Implements fxrates serve, running uvicorn on 127.0.0.1 in the foreground and stopping cleanly on SIGTERM. |
| Depends On | FEATURE-CliFoundation.md, FEATURE-UsageErrors.md, FEATURE-Health.md |
| Provides | fxrates serve |
| Consumes | GET /health, fxrates usage validation, cli.main |

## Purpose

`fxrates serve [--port <n>]` serves the HTTP API from `app_server.main:app` with uvicorn until stopped.

## Behavior

| Aspect | Rule |
|--------|------|
| Host | Bound only to `127.0.0.1`. |
| Port | `--port <n>`; default `8000`. A non-integer port is rejected earlier by usage validation with exit 2. |
| Foreground | The command runs in the foreground until stopped. |
| SIGTERM | uvicorn shuts down gracefully and the process exits 0. |
| Stdout | Nothing is required. |
| Schema | Serving never initializes the schema. |

The handler is `cli/commands/serve.py` with `run(args) -> int`.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC serve-health-reachable ===
Intent: Starting fxrates serve on a free local port makes GET /health answer 200 with the status ok body at 127.0.0.1 within a deadline, and the child is always terminated and reaped.
Requires: executable=python3; scope=test

import json
import os
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

sock = socket.socket()
sock.bind(("127.0.0.1", 0))
port = sock.getsockname()[1]
sock.close()

with tempfile.TemporaryDirectory() as tmp:
    env = {**os.environ, "DATABASE_URL": os.path.join(tmp, "serve.db")}
    log = open(os.path.join(tmp, "server.log"), "w+")
    child = subprocess.Popen(
        ["./fxrates", "serve", "--port", str(port)],
        stdout=log, stderr=subprocess.STDOUT, env=env,
    )
    try:
        url = f"http://127.0.0.1:{port}/health"
        deadline = time.time() + 30
        status = None
        body = None
        while time.time() < deadline:
            if child.poll() is not None:
                break
            try:
                with urllib.request.urlopen(url, timeout=2) as r:
                    status, body = r.status, json.loads(r.read())
                break
            except Exception:
                time.sleep(0.25)
        log.seek(0)
        print(log.read(), file=sys.stderr)
        assert child.poll() is None, "server exited before answering"
        assert status == 200
        assert body == {"status": "ok"}
    finally:
        if child.poll() is None:
            child.terminate()
        try:
            child.wait(timeout=15)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait()
        log.close()
=== END AC serve-health-reachable ===

=== AC serve-sigterm-clean ===
Intent: Sending SIGTERM to a running server stops it within a deadline with exit status 0.
Requires: executable=python3; scope=test

import os
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

sock = socket.socket()
sock.bind(("127.0.0.1", 0))
port = sock.getsockname()[1]
sock.close()

with tempfile.TemporaryDirectory() as tmp:
    env = {**os.environ, "DATABASE_URL": os.path.join(tmp, "serve.db")}
    child = subprocess.Popen(
        ["./fxrates", "serve", "--port", str(port)],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=env,
    )
    try:
        url = f"http://127.0.0.1:{port}/health"
        deadline = time.time() + 30
        ready = False
        while time.time() < deadline and child.poll() is None:
            try:
                with urllib.request.urlopen(url, timeout=2) as r:
                    ready = r.status == 200
                break
            except Exception:
                time.sleep(0.25)
        assert ready, "server never became ready"
        child.send_signal(signal.SIGTERM)
        code = child.wait(timeout=20)
        err = child.stderr.read().decode("utf-8", "replace")
        print(err, file=sys.stderr)
        assert code == 0
    finally:
        if child.poll() is None:
            child.kill()
            child.wait()
        child.stderr.close()
=== END AC serve-sigterm-clean ===

=== AC serve-bad-port-usage ===
Intent: A non-integer --port is a usage error that exits 2 with empty stdout and never starts a server.
Requires: executable=python3; scope=test

import subprocess

result = subprocess.run(
    ["./fxrates", "serve", "--port", "notaport"],
    capture_output=True, text=True, timeout=30,
)
print(result.stdout)
print(result.stderr)
assert result.returncode == 2
assert result.stdout == ""
=== END AC serve-bad-port-usage ===

## User Acceptance

- None.

## Guardrails

- The server binds only to `127.0.0.1`.
- Serving never initializes the schema; only `fxrates init` does.
- Acceptance always terminates and reaps the child process it starts.
