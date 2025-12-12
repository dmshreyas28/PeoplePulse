"""Application configuration management."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    database_url: str = "postgresql://postgres:postgres@localhost:5432/peoplepulse"
    secret_key: str = "change-this-secret-key"
    model_path: str = "./models/model.pkl"
    mlflow_tracking_uri: str = "http://localhost:5000"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
