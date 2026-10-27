"""Shared pytest fixtures for the CLI and web foundations."""

import pytest

from app_server import testing as web_testing
from cli import testing as cli_testing


@pytest.fixture
def cli_runner():
    return cli_testing.cli_runner


@pytest.fixture
def web_client():
    return web_testing.web_client()
