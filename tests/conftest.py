import pytest
from fastapi.testclient import TestClient

# Será implementado quando tivermos acesso ao arquivo principal da API
@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)

@pytest.fixture
def test_headers():
    return {
        "X-API-Key": "test_key",
        "Content-Type": "application/json"
    } 