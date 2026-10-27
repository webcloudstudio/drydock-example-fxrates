"""The `serve` command: run the HTTP API in the foreground on 127.0.0.1 until SIGTERM or SIGINT.

The port is validated by `cli.usage` before dispatch. Before uvicorn binds, this command probes the
port, so a port already in use exits 1 with one stderr line and answers no requests. Uvicorn's own
signal capture is replaced: it re-raises a captured SIGTERM after shutdown, which would end the
process by signal instead of with exit 0. Here the signal only asks the server to stop.
"""

from __future__ import annotations

import contextlib
import signal
import socket
import sys
from collections.abc import Callable, Iterator
from types import FrameType

import uvicorn

from cli.dispatcher import register_command
from cli.help import print_help

HOST = "127.0.0.1"
DEFAULT_PORT = 8000
APP_PATH = "app_server.main:app"
OPERATIONAL_FAILURE = 1
HELP_FLAG = "--help"
PORT_FLAG = "--port"
STOP_SIGNALS = (signal.SIGTERM, signal.SIGINT)


class _ForegroundServer(uvicorn.Server):
    """Uvicorn server that leaves signal handling to `serve`."""

    @contextlib.contextmanager
    def capture_signals(self) -> Iterator[None]:
        yield


def _port_is_free(port: int) -> bool:
    """Bind the port the way uvicorn does, then release it. True when nothing else holds it."""
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        probe.bind((HOST, port))
    except OSError:
        return False
    finally:
        probe.close()
    return True


def _requested_port(rest: list[str]) -> int:
    """Return the port named by `--port <n>`, or the default when no option is given."""
    return int(rest[1]) if rest else DEFAULT_PORT


def _stop_on(server: uvicorn.Server) -> Callable[[int, FrameType | None], None]:
    def handle(_signum: int, _frame: FrameType | None) -> None:
        server.should_exit = True

    return handle


def serve(rest: list[str]) -> int:
    """Serve the application until a stop signal; return 0 on a clean stop, 1 if the port is taken."""
    if rest == [HELP_FLAG]:
        return print_help("serve")
    port = _requested_port(rest)
    if not _port_is_free(port):
        print(f"error: port {port} on {HOST} is already in use", file=sys.stderr)
        return OPERATIONAL_FAILURE

    server = _ForegroundServer(uvicorn.Config(APP_PATH, host=HOST, port=port))
    previous = {sig: signal.signal(sig, _stop_on(server)) for sig in STOP_SIGNALS}
    try:
        server.run()
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)
    return 0


register_command("serve", serve)
