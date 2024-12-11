import pytest
from pydantic import ValidationError
from app.core.config import Settings

def test_settings_default_values():
    """Testa se os valores padrão são configurados corretamente"""
    settings = Settings(
        API_KEY="test_key",
        SECRET_KEY="test_secret"
    )
    assert settings.APP_ENV == "development"

def test_settings_custom_values():
    """Testa se valores customizados são aceitos"""
    settings = Settings(
        APP_ENV="production",
        API_KEY="prod_key",
        SECRET_KEY="prod_secret"
    )
    assert settings.APP_ENV == "production"
    assert settings.API_KEY == "prod_key"
    assert settings.SECRET_KEY == "prod_secret"

def test_settings_missing_required_values():
    """Testa se erro é lançado quando valores obrigatórios estão ausentes"""
    with pytest.raises(ValidationError):
        Settings()

def test_settings_invalid_app_env():
    """Testa validação de APP_ENV com valor inválido"""
    with pytest.raises(ValidationError):
        Settings(
            APP_ENV="invalid",
            API_KEY="test_key",
            SECRET_KEY="test_secret"
        )

@pytest.mark.parametrize("env_value", ["development", "staging", "production"])
def test_settings_valid_app_envs(env_value):
    """Testa valores válidos para APP_ENV"""
    settings = Settings(
        APP_ENV=env_value,
        API_KEY="test_key",
        SECRET_KEY="test_secret"
    )
    assert settings.APP_ENV == env_value 