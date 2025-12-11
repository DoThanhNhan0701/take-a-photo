from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str
    
    # Application
    APP_NAME: str = "Take a Photo API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API for invoice photo management system"
    DEBUG: bool = False
    
    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    
    # Security & JWT
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
