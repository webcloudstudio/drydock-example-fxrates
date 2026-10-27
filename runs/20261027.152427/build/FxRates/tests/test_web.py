"""Application factory, module-level app, router registry, and the web_client fixture."""

from __future__ import annotations

import pytest
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

from app_server import routes
from app_server import testing as app_testing
from app_server.main import app, create_app


def test_create_app_returns_a_fastapi_instance() -> None:
    assert isinstance(create_app(), FastAPI)


def test_create_app_returns_a_new_instance_each_call() -> None:
    assert create_app() is not create_app()


def test_module_level_app_is_a_fastapi_instance() -> None:
    assert isinstance(app, FastAPI)


def test_router_registry_is_an_apirouter() -> None:
    assert isinstance(routes.router, APIRouter)


def test_routes_on_the_registry_are_served_by_created_apps(monkeypatch: pytest.MonkeyPatch) -> None:
    registry = APIRouter()

    @registry.get("/probe")
    def probe() -> dict[str, bool]:
        return {"ok": True}

    monkeypatch.setattr(routes, "router", registry)

    response = TestClient(create_app()).get("/probe")

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_web_client_returns_a_testclient_wrapping_a_fastapi_app() -> None:
    client = app_testing.web_client()

    assert isinstance(client, TestClient)
    assert isinstance(client.app, FastAPI)


def test_web_client_fixture_wraps_a_fastapi_app(web_client) -> None:
    assert isinstance(web_client, TestClient)
    assert isinstance(web_client.app, FastAPI)


def test_openapi_document_is_served_as_json(web_client) -> None:
    response = web_client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["openapi"].startswith("3.")


def test_docs_page_is_served(web_client) -> None:
    response = web_client.get("/docs")

    assert response.status_code == 200


def test_unknown_path_returns_not_found(web_client) -> None:
    response = web_client.get("/no-such-path")

    assert response.status_code == 404
