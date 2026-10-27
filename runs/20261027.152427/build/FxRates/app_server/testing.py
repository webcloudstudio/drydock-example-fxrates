"""In-process test client for the application; used by acceptance and the pytest suite."""

from fastapi.testclient import TestClient

from app_server.main import create_app


def web_client() -> TestClient:
    """Return a TestClient wrapping a new application instance."""
    return TestClient(create_app())
