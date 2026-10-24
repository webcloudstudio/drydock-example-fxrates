from persistence import open_database
from app_server.main import create_app
from fastapi.testclient import TestClient


def test_app_factory_health():
    response = TestClient(create_app()).get('/health')
    assert response.status_code == 200


def test_declared_rates_operations_exist():
    db = open_database('')
    assert hasattr(db, 'rates')
    assert callable(db.rates.list)
    assert callable(db.rates.upsert)
    assert callable(db.rates.delete)
