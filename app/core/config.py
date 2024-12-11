from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    API_KEY: str
    SECRET_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings() 