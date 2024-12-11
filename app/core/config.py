from enum import Enum
from pydantic_settings import BaseSettings

class AppEnvironment(str, Enum):
    TEST = "test"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    APP_ENV: AppEnvironment = AppEnvironment.DEVELOPMENT
    API_KEY: str = "test_key"  # Apenas para desenvolvimento
    SECRET_KEY: str = "test_secret"  # Apenas para desenvolvimento
    
    # Redis
    REDIS_URL: str = "redis://localhost"
    REDIS_CACHE_TTL: int = 3600  # 1 hora
    
    # Cache
    CACHE_ENABLED: bool = True
    
    class Config:
        env_file = ".env"
        use_enum_values = True
        case_sensitive = True

settings = Settings() 