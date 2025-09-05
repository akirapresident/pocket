"""
Pocket - Configuration Settings
Fase 1: Basic configuration for Instagram scraping
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Instagram Credentials
    instagram_username: str = ""
    instagram_password: str = ""
    
    # Database
    database_url: str = "sqlite:///./pocket.db"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = True
    
    # Scraping Configuration
    scraping_delay: int = 2
    max_retries: int = 3
    session_timeout: int = 300
    
    # File Storage
    upload_dir: str = "./uploads"
    export_dir: str = "./exports"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/pocket.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings
