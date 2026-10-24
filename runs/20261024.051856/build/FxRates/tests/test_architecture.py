"""Architecture boundary checks for the foundational application modules."""

import importlib


def test_published_application_modules_are_importable() -> None:
    for name in ("cli", "app_server", "persistence"):
        module = importlib.import_module(name)
        assert module is not None
