"""Application configuration settings."""

from typing import Optional, List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "ImmersiVerse OS Backend"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # API
    api_v1_prefix: str = "/api/v1"
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Database
    database_url: str = "postgresql://user:password@localhost/immersiverse"
    database_echo: bool = False
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    redis_db: int = 0
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # External Services
    unity_client_timeout: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
