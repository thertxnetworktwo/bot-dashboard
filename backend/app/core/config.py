from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://dashboard_user:your_secure_password@localhost:5432/dashboard_db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "dashboard_db"
    DB_USER: str = "dashboard_user"
    DB_PASSWORD: str = "your_secure_password"
    
    # API
    API_SECRET_KEY: str = "your-secret-key-min-32-chars-change-in-production"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    
    # CORS - Comma-separated list of allowed origins
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://localhost:7082"
    
    # Phone Registry (External)
    PHONE_REGISTRY_URL: str = "http://localhost:8000"
    PHONE_REGISTRY_API_KEY: str = "your-api-key"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # Environment
    ENV: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
