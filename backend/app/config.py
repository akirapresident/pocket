"""
Configuration settings for the Instagram Analytics Backend
"""
import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Instagram Analytics"
    VERSION: str = "1.0.0"
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./instagram_analytics.db")
    
    # Apify Configuration
    APIFY_TOKEN: str = os.getenv("APIFY_TOKEN", "YOUR_APIFY_TOKEN_HERE")
    APIFY_ACTOR_ID: str = "apify~instagram-scraper"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
    ]

settings = Settings()
