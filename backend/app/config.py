"""Application configuration management."""
import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""

    database_url: str = "sqlite:///./test.db"
    secret_key: str = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    model_path: str = "ml/models/model.pkl"
    mlflow_tracking_uri: str = "http://localhost:5000"
    debug: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
