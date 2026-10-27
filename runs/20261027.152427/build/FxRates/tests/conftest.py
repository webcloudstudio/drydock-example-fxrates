"""Shared pytest fixtures for the FxRates suite.

Tests never open a network connection. Any attempt to connect a socket fails the test, so an
accidental download cannot slip through a suite that is meant to run offline.
"""

from __future__ import annotations

import socket
from collections.abc import Iterator
from pathlib import Path

import pytest

from app_server import testing as app_testing
from cli import testing as cli_testing


class NetworkAccessError(RuntimeError):
    """Raised when a test attempts to open a network connection."""


def _refuse_connection(*_args: object, **_kwargs: object) -> None:
    raise NetworkAccessError("tests must not open network connections")


@pytest.fixture(autouse=True)
def _block_network(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.setattr(socket.socket, "connect", _refuse_connection)
    monkeypatch.setattr(socket, "create_connection", _refuse_connection)
    yield


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def cli_runner():
    return cli_testing.cli_runner


@pytest.fixture
def web_client():
    return app_testing.web_client()
