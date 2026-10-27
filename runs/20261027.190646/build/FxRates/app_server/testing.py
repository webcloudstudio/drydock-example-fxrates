"""In-process HTTP client for tests. No server is started and no socket is opened."""

from fastapi.testclient import TestClient

from app_server.main import create_app


def web_client() -> TestClient:
    """Return a test client over a freshly built application."""
    return TestClient(create_app())
