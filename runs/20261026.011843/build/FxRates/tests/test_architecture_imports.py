from app_server.main import create_app
from cli import main


def test_architecture_entry_points_are_importable():
    assert callable(create_app)
    assert callable(main)
