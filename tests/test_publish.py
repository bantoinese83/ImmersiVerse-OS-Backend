"""Tests for publishing endpoints."""

import pytest
from fastapi import status


def test_publish_experience(client, auth_headers, sample_world_blueprint):
    """Test publishing a world blueprint as an experience."""
    # First create a world blueprint
    world_request = {
        "prompt": "A magical forest with ancient trees",
        "world_type": "fantasy",
        "user_id": "test_user"
    }
    
    world_response = client.post("/api/v1/prompt2world/", json=world_request, headers=auth_headers)
    assert world_response.status_code == status.HTTP_200_OK
    world_id = world_response.json()["world_blueprint"]["id"]
    
    # Now publish the experience
    publish_request = {
        "world_blueprint_id": world_id,
        "title": "Magical Forest Experience",
        "description": "Explore a mystical forest filled with ancient trees",
        "tags": ["fantasy", "forest", "magic"],
        "is_public": True,
        "user_id": "test_user"
    }
    
    response = client.post("/api/v1/publish/", json=publish_request, headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert "experience_card" in data
    assert data["experience_card"]["title"] == publish_request["title"]
    assert data["experience_card"]["world_blueprint_id"] == world_id


def test_publish_experience_invalid_world_id(client, auth_headers):
    """Test publishing with non-existent world blueprint ID."""
    publish_request = {
        "world_blueprint_id": "non_existent_id",
        "title": "Test Experience",
        "description": "Test description",
        "user_id": "test_user"
    }
    
    response = client.post("/api/v1/publish/", json=publish_request, headers=auth_headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_publish_experience_unauthorized(client):
    """Test publishing without authentication."""
    publish_request = {
        "world_blueprint_id": "some_id",
        "title": "Test Experience",
        "description": "Test description",
        "user_id": "test_user"
    }
    
    response = client.post("/api/v1/publish/", json=publish_request)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_public_experiences(client, auth_headers):
    """Test getting list of public experiences."""
    response = client.get("/api/v1/publish/experiences", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)


def test_get_experience_by_id(client, auth_headers):
    """Test getting a specific experience by ID."""
    # First create and publish an experience
    world_request = {
        "prompt": "A test world",
        "user_id": "test_user"
    }
    
    world_response = client.post("/api/v1/prompt2world/", json=world_request, headers=auth_headers)
    world_id = world_response.json()["world_blueprint"]["id"]
    
    publish_request = {
        "world_blueprint_id": world_id,
        "title": "Test Experience",
        "description": "Test description",
        "user_id": "test_user"
    }
    
    publish_response = client.post("/api/v1/publish/", json=publish_request, headers=auth_headers)
    experience_id = publish_response.json()["experience_card"]["id"]
    
    # Now get the experience
    response = client.get(f"/api/v1/publish/experiences/{experience_id}", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["experience_card"]["id"] == experience_id


def test_get_experience_by_id_not_found(client, auth_headers):
    """Test getting non-existent experience by ID."""
    response = client.get("/api/v1/publish/experiences/non_existent_id", headers=auth_headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
