import importlib


def test_architecture_entry_modules_are_importable():
    for module_name in ("app_server.main", "cli", "persistence"):
        assert importlib.import_module(module_name) is not None


def test_application_and_cli_entry_points_are_callable():
    from app_server.main import create_app
    from cli import main

    assert callable(create_app)
    assert callable(main)


def test_application_factory_returns_fastapi_application():
    from fastapi import FastAPI

    from app_server.main import create_app

    assert isinstance(create_app(), FastAPI)
