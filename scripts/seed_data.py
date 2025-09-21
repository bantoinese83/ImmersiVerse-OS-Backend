#!/usr/bin/env python3
"""Script to seed the database with initial data."""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base
from app.services.prefab_service import PrefabService


def seed_database():
    """Seed the database with initial data."""
    print("🌱 Seeding database with initial data...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    # Create database session
    db: Session = SessionLocal()
    
    try:
        # Seed prefab catalog
        prefab_service = PrefabService(db)
        prefab_service.seed_default_prefabs()
        print("✅ Prefab catalog seeded")
        
        print("🎉 Database seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
