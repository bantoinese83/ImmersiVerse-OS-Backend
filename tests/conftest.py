"""Test configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_database_session, Base
from app.config import settings

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override settings for testing
import os
os.environ["DATABASE_URL"] = SQLALCHEMY_DATABASE_URL


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override."""
    app.dependency_overrides[get_database_session] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    """Create authentication headers for testing."""
    # Create a test session
    response = client.post("/api/v1/auth/login", json={"user_id": "test_user"})
    assert response.status_code == 200
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_world_blueprint():
    """Sample world blueprint for testing."""
    from app.schemas import WorldBlueprint, WorldType, Vector3, PrefabInstance, PrefabType, Quaternion
    
    return WorldBlueprint(
        prompt="A magical forest with ancient trees",
        world_type=WorldType.FANTASY,
        title="Magical Forest World",
        description="A mystical forest filled with ancient trees and magical creatures",
        environment_settings={"lighting": "mystical", "weather": "ethereal"},
        prefab_instances=[
            PrefabInstance(
                prefab_id="magic_tree_01",
                prefab_type=PrefabType.ENVIRONMENT,
                position=Vector3(x=0, y=0, z=0),
                rotation=Quaternion(x=0, y=0, z=0, w=1)
            )
        ],
        spawn_points=[Vector3(x=0, y=1, z=0)]
    )


@pytest.fixture
def sample_telemetry_event():
    """Sample telemetry event for testing."""
    from app.schemas import TelemetryEvent
    from datetime import datetime
    
    return TelemetryEvent(
        event_type="world_entered",
        user_id="test_user",
        session_id="test_session",
        world_id="test_world",
        data={"action": "enter", "timestamp": datetime.utcnow().isoformat()},
        timestamp=datetime.utcnow()
    )
