import pytest
from fastapi.testclient import TestClient
from app.core.config import Settings
from app.main import app

@pytest.fixture
def test_settings():
    return Settings(
        APP_ENV="development",
        API_KEY="test_key",
        SECRET_KEY="test_secret"
    )

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_headers():
    return {
        "X-API-Key": "test_key",
        "Content-Type": "application/json"
    }

@pytest.fixture
def api_base_url():
    return "/api/v1" 