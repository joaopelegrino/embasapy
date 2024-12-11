import pytest
from fastapi import HTTPException, Security
from app.core.security import get_api_key, api_key_header
from app.core.config import Settings

@pytest.fixture
def valid_api_key():
    return "test_key"

@pytest.fixture
def invalid_api_key():
    return "invalid_key"

async def test_valid_api_key(valid_api_key):
    """Testa validação de API Key válida"""
    result = await get_api_key(valid_api_key)
    assert result == valid_api_key

async def test_invalid_api_key(invalid_api_key):
    """Testa rejeição de API Key inválida"""
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(invalid_api_key)
    assert exc_info.value.status_code == 403
    assert "Could not validate API key" in exc_info.value.detail

async def test_missing_api_key():
    """Testa quando API Key não é fornecida"""
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(None)
    assert exc_info.value.status_code == 403
    assert "Could not validate API key" in exc_info.value.detail

def test_api_key_header_configuration():
    """Testa configuração do header da API Key"""
    assert api_key_header.scheme_name == "API Key"
    assert api_key_header.name == "X-API-Key"
    assert api_key_header.auto_error is False

@pytest.mark.parametrize("api_key", ["", " ", "\t", "\n"])
async def test_empty_api_key(api_key):
    """Testa rejeição de API Keys vazias ou com whitespace"""
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(api_key)
    assert exc_info.value.status_code == 403 