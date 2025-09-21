"""Tests for authentication endpoints."""

import pytest
from fastapi import status


def test_create_session(client):
    """Test creating a new user session."""
    response = client.post("/api/v1/auth/login", json={"user_id": "test_user"})
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "token" in data
    assert "session_id" in data
    assert data["user_id"] == "test_user"
    assert "expires_at" in data


def test_create_session_invalid_user_id(client):
    """Test creating session with invalid user ID."""
    response = client.post("/api/v1/auth/login", json={"user_id": ""})
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_validate_session(client, auth_headers):
    """Test validating a session token."""
    response = client.get("/api/v1/auth/validate", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["valid"] is True
    assert data["user_id"] == "test_user"
    assert "session_id" in data


def test_validate_session_invalid_token(client):
    """Test validating an invalid session token."""
    response = client.get("/api/v1/auth/validate", headers={"Authorization": "Bearer invalid_token"})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_validate_session_missing_header(client):
    """Test validating session without authorization header."""
    response = client.get("/api/v1/auth/validate")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout_session(client, auth_headers):
    """Test logging out a session."""
    response = client.post("/api/v1/auth/logout", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True


def test_logout_session_invalid_token(client):
    """Test logging out with invalid token."""
    response = client.post("/api/v1/auth/logout", headers={"Authorization": "Bearer invalid_token"})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
