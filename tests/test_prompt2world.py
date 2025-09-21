"""Tests for prompt to world conversion endpoint."""

import pytest
from fastapi import status


def test_convert_prompt_to_world(client, auth_headers):
    """Test converting a prompt to a world blueprint."""
    request_data = {
        "prompt": "A magical forest with ancient trees and glowing mushrooms",
        "world_type": "fantasy",
        "user_id": "test_user"
    }
    
    response = client.post("/api/v1/prompt2world/", json=request_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert "world_blueprint" in data
    assert data["world_blueprint"]["prompt"] == request_data["prompt"]
    assert data["world_blueprint"]["world_type"] == request_data["world_type"]
    assert "prefab_instances" in data["world_blueprint"]
    assert "spawn_points" in data["world_blueprint"]
    assert "processing_time_ms" in data


def test_convert_prompt_to_world_auto_infer_type(client, auth_headers):
    """Test converting a prompt with auto-inferred world type."""
    request_data = {
        "prompt": "A futuristic space station with alien technology",
        "user_id": "test_user"
    }
    
    response = client.post("/api/v1/prompt2world/", json=request_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["world_blueprint"]["world_type"] == "sci_fi"  # Should be auto-inferred


def test_convert_prompt_to_world_invalid_prompt(client, auth_headers):
    """Test converting with invalid prompt."""
    request_data = {
        "prompt": "",  # Empty prompt
        "user_id": "test_user"
    }
    
    response = client.post("/api/v1/prompt2world/", json=request_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_convert_prompt_to_world_unauthorized(client):
    """Test converting prompt without authentication."""
    request_data = {
        "prompt": "A magical forest",
        "user_id": "test_user"
    }
    
    response = client.post("/api/v1/prompt2world/", json=request_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_convert_prompt_to_world_long_prompt(client, auth_headers):
    """Test converting with a very long prompt."""
    long_prompt = "A magical forest " * 100  # Very long prompt
    
    request_data = {
        "prompt": long_prompt,
        "user_id": "test_user"
    }
    
    response = client.post("/api/v1/prompt2world/", json=request_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # Should exceed max length
