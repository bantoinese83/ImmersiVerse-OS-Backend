"""SQLAlchemy database models."""

from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, Float, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class WorldBlueprintModel(Base):
    """Database model for world blueprints."""
    __tablename__ = "world_blueprints"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    prompt = Column(Text, nullable=False)
    world_type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    environment_settings = Column(JSON, default=dict)
    prefab_instances = Column(JSON, default=list)
    spawn_points = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    experiences = relationship("ExperienceCardModel", back_populates="world_blueprint")


class ExperienceCardModel(Base):
    """Database model for experience cards."""
    __tablename__ = "experience_cards"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    world_blueprint_id = Column(String, ForeignKey("world_blueprints.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    tags = Column(JSON, default=list)
    author_id = Column(String(100), nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)
    play_count = Column(Integer, default=0, nullable=False)
    rating = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    world_blueprint = relationship("WorldBlueprintModel", back_populates="experiences")


class PrefabCatalogModel(Base):
    """Database model for prefab catalog items."""
    __tablename__ = "prefab_catalog"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    download_url = Column(String(500), nullable=False)
    size_bytes = Column(Integer, nullable=False)
    version = Column(String(50), nullable=False)
    tags = Column(JSON, default=list)
    properties = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class TelemetryEventModel(Base):
    """Database model for telemetry events."""
    __tablename__ = "telemetry_events"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type = Column(String(100), nullable=False)
    user_id = Column(String(100), nullable=False)
    session_id = Column(String(100), nullable=False)
    world_id = Column(String(100), nullable=True)
    experience_id = Column(String(100), nullable=True)
    data = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)


class UserSessionModel(Base):
    """Database model for user sessions."""
    __tablename__ = "user_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(100), nullable=False, index=True)
    session_id = Column(String(100), nullable=False, unique=True, index=True)
    token = Column(String(500), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
