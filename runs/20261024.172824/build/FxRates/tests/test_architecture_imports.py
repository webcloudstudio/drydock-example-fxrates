"""Declared architecture importability contract."""

from app_server.main import app, create_app
from app_server.testing import web_client
from cli import main
from cli.testing import cli_runner


def test_application_and_command_entry_points_are_importable() -> None:
    assert callable(create_app)
    assert app is not None
    assert callable(web_client)
    assert callable(main)
    assert callable(cli_runner)
