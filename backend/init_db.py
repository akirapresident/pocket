#!/usr/bin/env python3
"""
Initialize database and create tables
"""
from app.utils.database import create_tables
from app.models import video, profile  # Import models to register them

if __name__ == "__main__":
    print("🚀 Initializing database...")
    create_tables()
    print("✅ Database initialized successfully!")
