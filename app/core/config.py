from enum import Enum
from pydantic_settings import BaseSettings

class AppEnvironment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    APP_ENV: AppEnvironment = AppEnvironment.DEVELOPMENT
    API_KEY: str
    SECRET_KEY: str
    
    # Redis
    REDIS_URL: str = "redis://localhost"
    REDIS_CACHE_TTL: int = 3600  # 1 hora
    
    class Config:
        env_file = ".env"
        use_enum_values = True

settings = Settings() 