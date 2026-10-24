"""In-process HTTP testing helper."""

from fastapi.testclient import TestClient

from app_server.main import create_app


def web_client() -> TestClient:
    """Return a client for a fresh application instance."""
    return TestClient(create_app())
