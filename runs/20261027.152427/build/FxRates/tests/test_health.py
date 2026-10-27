"""Health route and the served documentation, read back through the in-process web client."""

from __future__ import annotations


def test_health_returns_status_ok(web_client) -> None:
    response = web_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_answers_on_every_call(web_client) -> None:
    first = web_client.get("/health").json()
    second = web_client.get("/health").json()

    assert first == second == {"status": "ok"}


def test_health_rejects_post(web_client) -> None:
    response = web_client.post("/health")

    assert response.status_code == 405


def test_openapi_document_lists_health_path(web_client) -> None:
    spec = web_client.get("/openapi.json").json()

    assert "/health" in spec["paths"]
    assert "get" in spec["paths"]["/health"]


def test_docs_page_is_served_as_html(web_client) -> None:
    response = web_client.get("/docs")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
