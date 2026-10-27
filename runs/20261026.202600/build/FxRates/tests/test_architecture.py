"""Architecture boundary smoke checks."""

import importlib.util


def test_services_is_importable_boundary() -> None:
    assert importlib.util.find_spec("services") is not None
