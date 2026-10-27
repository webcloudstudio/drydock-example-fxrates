"""The `serve` handler checks that run before uvicorn binds, exercised in-process.

The live listen-and-SIGTERM behavior is the declared acceptance criterion `serve-live-sigterm`, which
runs the launcher in a subprocess; starting a server here would need the network the suite blocks.
"""

from __future__ import annotations

import socket
from collections.abc import Iterator

import pytest

from cli import dispatcher, serve_command


@pytest.fixture
def busy_port() -> Iterator[int]:
    """A port held by a listening socket for the duration of the test."""
    blocker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        blocker.bind(("127.0.0.1", 0))
        blocker.listen(1)
        yield blocker.getsockname()[1]
    finally:
        blocker.close()


@pytest.fixture
def free_port() -> int:
    """A port that nothing holds at the moment the test starts."""
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]
    finally:
        probe.close()


def test_serve_is_registered_with_the_dispatcher() -> None:
    assert dispatcher._handlers["serve"] is serve_command.serve


def test_busy_port_exits_1_with_empty_stdout(cli_runner, busy_port: int) -> None:
    code, out, _err = cli_runner("serve", "--port", str(busy_port))

    assert code == 1
    assert out == ""


def test_busy_port_writes_one_stderr_line(cli_runner, busy_port: int) -> None:
    _code, _out, err = cli_runner("serve", "--port", str(busy_port))

    assert len(err.strip().splitlines()) == 1


def test_busy_port_error_names_the_port(cli_runner, busy_port: int) -> None:
    _code, _out, err = cli_runner("serve", "--port", str(busy_port))

    assert str(busy_port) in err


def test_port_probe_reports_a_busy_port_as_taken(busy_port: int) -> None:
    assert serve_command._port_is_free(busy_port) is False


def test_port_probe_reports_a_free_port_as_available(free_port: int) -> None:
    assert serve_command._port_is_free(free_port) is True


def test_port_probe_leaves_the_port_free_after_it_runs(free_port: int) -> None:
    serve_command._port_is_free(free_port)

    assert serve_command._port_is_free(free_port) is True


def test_default_port_is_8000() -> None:
    assert serve_command._requested_port([]) == 8000


def test_explicit_port_is_read_from_the_option() -> None:
    assert serve_command._requested_port(["--port", "8123"]) == 8123


def test_help_flag_returns_0_without_binding(cli_runner) -> None:
    code, out, err = cli_runner("serve", "--help")

    assert code == 0
    assert out.splitlines()[0] == "usage: fxrates serve [--port <n>]"
    assert err == ""
