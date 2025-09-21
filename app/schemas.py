"""Pydantic schemas for data validation and serialization."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class WorldType(str, Enum):
    """Types of worlds that can be generated."""
    FANTASY = "fantasy"
    SCI_FI = "sci_fi"
    REALISTIC = "realistic"
    SURREAL = "surreal"
    HISTORICAL = "historical"
    URBAN = "urban"
    NATURE = "nature"
    SPACE = "space"


class PrefabType(str, Enum):
    """Types of prefabs available in the Unity catalog."""
    BUILDING = "building"
    VEHICLE = "vehicle"
    CHARACTER = "character"
    PROP = "prop"
    ENVIRONMENT = "environment"
    LIGHTING = "lighting"
    EFFECT = "effect"
    UI = "ui"


class Vector3(BaseModel):
    """3D vector representation for Unity coordinates."""
    x: float = Field(..., description="X coordinate")
    y: float = Field(..., description="Y coordinate")
    z: float = Field(..., description="Z coordinate")


class Quaternion(BaseModel):
    """Quaternion representation for Unity rotations."""
    x: float = Field(..., description="X component")
    y: float = Field(..., description="Y component")
    z: float = Field(..., description="Z component")
    w: float = Field(..., description="W component")


class PrefabInstance(BaseModel):
    """Represents a prefab instance in the world."""
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique instance ID")
    prefab_id: str = Field(..., description="ID of the prefab from catalog")
    prefab_type: PrefabType = Field(..., description="Type of prefab")
    position: Vector3 = Field(..., description="World position")
    rotation: Quaternion = Field(..., description="World rotation")
    scale: Vector3 = Field(default_factory=lambda: Vector3(x=1.0, y=1.0, z=1.0), description="Scale")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Custom properties")


class WorldBlueprint(BaseModel):
    """Complete blueprint for generating a world."""
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique blueprint ID")
    prompt: str = Field(..., min_length=1, max_length=1000, description="Original text prompt")
    world_type: WorldType = Field(..., description="Type of world to generate")
    title: str = Field(..., min_length=1, max_length=200, description="World title")
    description: str = Field(..., min_length=1, max_length=2000, description="World description")
    environment_settings: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Environment configuration (lighting, weather, etc.)"
    )
    prefab_instances: List[PrefabInstance] = Field(
        default_factory=list, 
        description="List of prefab instances in the world"
    )
    spawn_points: List[Vector3] = Field(
        default_factory=list, 
        description="Player spawn points"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    processing_time_ms: Optional[int] = Field(None, description="Processing time in milliseconds")
    
    @field_validator('prefab_instances')
    @classmethod
    def validate_prefab_instances(cls, v: List[PrefabInstance]) -> List[PrefabInstance]:
        """Validate prefab instances have unique IDs."""
        instance_ids = [instance.id for instance in v]
        if len(instance_ids) != len(set(instance_ids)):
            raise ValueError("Prefab instances must have unique IDs")
        return v


class ExperienceCard(BaseModel):
    """Card representing a published experience."""
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique experience ID")
    world_blueprint_id: str = Field(..., description="Reference to world blueprint")
    title: str = Field(..., min_length=1, max_length=200, description="Experience title")
    description: str = Field(..., min_length=1, max_length=2000, description="Experience description")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail image URL")
    tags: List[str] = Field(default_factory=list, description="Search tags")
    author_id: str = Field(..., description="Author user ID")
    is_public: bool = Field(default=True, description="Whether experience is public")
    play_count: int = Field(default=0, description="Number of times played")
    rating: Optional[float] = Field(None, ge=0.0, le=5.0, description="Average rating")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")


class PrefabCatalogItem(BaseModel):
    """Item in the Unity prefab catalog."""
    id: str = Field(..., description="Unique prefab ID")
    name: str = Field(..., description="Prefab name")
    type: PrefabType = Field(..., description="Prefab type")
    description: str = Field(..., description="Prefab description")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail image URL")
    download_url: str = Field(..., description="URL to download prefab")
    size_bytes: int = Field(..., description="Prefab file size in bytes")
    version: str = Field(..., description="Prefab version")
    tags: List[str] = Field(default_factory=list, description="Search tags")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Prefab properties")


class PromptRequest(BaseModel):
    """Request to convert a text prompt to a world blueprint."""
    prompt: str = Field(..., min_length=1, max_length=1000, description="Text prompt")
    world_type: Optional[WorldType] = Field(None, description="Preferred world type")
    user_id: str = Field(..., description="User ID making the request")


class PublishRequest(BaseModel):
    """Request to publish a world blueprint as an experience."""
    world_blueprint_id: str = Field(..., description="World blueprint ID to publish")
    title: str = Field(..., min_length=1, max_length=200, description="Experience title")
    description: str = Field(..., min_length=1, max_length=2000, description="Experience description")
    tags: List[str] = Field(default_factory=list, description="Search tags")
    is_public: bool = Field(default=True, description="Whether to make public")
    user_id: str = Field(..., description="User ID publishing the experience")


class TelemetryEvent(BaseModel):
    """Telemetry event data."""
    event_type: str = Field(..., description="Type of event")
    user_id: str = Field(..., description="User ID")
    session_id: str = Field(..., description="Session ID")
    world_id: Optional[str] = Field(None, description="World ID if applicable")
    experience_id: Optional[str] = Field(None, description="Experience ID if applicable")
    data: Dict[str, Any] = Field(default_factory=dict, description="Event-specific data")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Event timestamp")


class UserSession(BaseModel):
    """User session information."""
    user_id: str = Field(..., description="User ID")
    session_id: str = Field(default_factory=lambda: str(uuid4()), description="Session ID")
    token: str = Field(..., description="Session token")
    expires_at: datetime = Field(..., description="Token expiration time")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Session creation time")


# Response schemas
class PromptResponse(BaseModel):
    """Response for prompt to world conversion."""
    success: bool = Field(..., description="Whether conversion was successful")
    world_blueprint: Optional[WorldBlueprint] = Field(None, description="Generated world blueprint")
    message: str = Field(..., description="Response message")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")


class PublishResponse(BaseModel):
    """Response for publishing an experience."""
    success: bool = Field(..., description="Whether publishing was successful")
    experience_card: Optional[ExperienceCard] = Field(None, description="Created experience card")
    message: str = Field(..., description="Response message")


class TelemetryResponse(BaseModel):
    """Response for telemetry submission."""
    success: bool = Field(..., description="Whether submission was successful")
    message: str = Field(..., description="Response message")


class PrefabCatalogResponse(BaseModel):
    """Response for prefab catalog requests."""
    success: bool = Field(..., description="Whether request was successful")
    prefabs: List[PrefabCatalogItem] = Field(..., description="List of prefab items")
    total_count: int = Field(..., description="Total number of prefabs")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
