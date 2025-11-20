"""
Configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/promptcrawler"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # API Keys
    PERPLEXITY_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://*.railway.app",
        "https://*.up.railway.app"
    ]
    
    # App
    BACKEND_PORT: int = 8000
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

