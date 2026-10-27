"""Published in-process FastAPI test client factory."""

from fastapi.testclient import TestClient

from app_server.main import create_app


def web_client() -> TestClient:
    return TestClient(create_app())
