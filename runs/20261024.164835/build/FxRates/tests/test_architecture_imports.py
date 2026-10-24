"""Import checks for the declared application boundaries."""

import importlib


def test_configuration_and_service_boundaries_import():
    for module_name in ("config", "services"):
        assert importlib.import_module(module_name) is not None


def test_cli_and_http_boundaries_are_importable():
    for module_name in ("cli", "app_server"):
        assert importlib.import_module(module_name) is not None
