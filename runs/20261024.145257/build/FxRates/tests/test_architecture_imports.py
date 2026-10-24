import app_server.main
import cli


def test_application_entry_points_import_and_are_callable():
    assert callable(cli.main)
    assert callable(app_server.main.create_app)
