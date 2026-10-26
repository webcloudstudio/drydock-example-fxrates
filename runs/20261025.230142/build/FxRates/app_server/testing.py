"""In-process HTTP client for application acceptance checks."""

from fastapi.testclient import TestClient

from app_server.main import create_app


def web_client() -> TestClient:
    """Return a test client for a newly created application."""
    return TestClient(create_app())
