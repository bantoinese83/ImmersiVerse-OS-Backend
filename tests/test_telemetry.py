"""Tests for telemetry endpoints."""

import pytest
from fastapi import status


def test_log_telemetry_event(client, auth_headers, sample_telemetry_event):
    """Test logging a single telemetry event."""
    event_data = sample_telemetry_event.model_dump()
    
    response = client.post("/api/v1/telemetry/", json=event_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert "logged successfully" in data["message"]


def test_log_telemetry_events_batch(client, auth_headers):
    """Test logging multiple telemetry events."""
    events_data = [
        {
            "event_type": "world_entered",
            "user_id": "test_user",
            "session_id": "test_session",
            "world_id": "test_world_1",
            "data": {"action": "enter"}
        },
        {
            "event_type": "prefab_instantiated",
            "user_id": "test_user",
            "session_id": "test_session",
            "world_id": "test_world_1",
            "data": {"prefab_id": "magic_tree_01"}
        }
    ]
    
    response = client.post("/api/v1/telemetry/batch", json=events_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert "2 telemetry events" in data["message"]


def test_log_telemetry_event_unauthorized(client, sample_telemetry_event):
    """Test logging telemetry event without authentication."""
    event_data = sample_telemetry_event.model_dump()
    
    response = client.post("/api/v1/telemetry/", json=event_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_user_events(client, auth_headers, sample_telemetry_event):
    """Test getting telemetry events for a user."""
    # First log an event
    event_data = sample_telemetry_event.model_dump()
    client.post("/api/v1/telemetry/", json=event_data, headers=auth_headers)
    
    # Then get user events
    response = client.get("/api/v1/telemetry/events/user/test_user", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["user_id"] == "test_user"


def test_get_user_events_unauthorized(client):
    """Test getting user events without authentication."""
    response = client.get("/api/v1/telemetry/events/user/test_user")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_user_events_forbidden(client, auth_headers):
    """Test getting events for another user (should be forbidden)."""
    response = client.get("/api/v1/telemetry/events/user/other_user", headers=auth_headers)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
