"""Tests for the declared foundational package and executable boundaries."""

import importlib.util
from pathlib import Path


def test_cli_package_is_importable() -> None:
    assert importlib.util.find_spec("cli") is not None


def test_app_server_package_is_importable() -> None:
    assert importlib.util.find_spec("app_server") is not None


def test_root_entrypoint_exists() -> None:
    assert Path("fxrates").is_file()


def test_cli_dispatch_returns_exit_code() -> None:
    from cli import main

    assert main([]) == 2
