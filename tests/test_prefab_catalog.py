"""Tests for prefab catalog endpoints."""

import pytest
from fastapi import status


def test_get_prefab_catalog(client, auth_headers):
    """Test getting the prefab catalog."""
    response = client.get("/api/v1/prefab-catalog/", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert "prefabs" in data
    assert "total_count" in data
    assert "page" in data
    assert "page_size" in data
    assert isinstance(data["prefabs"], list)


def test_get_prefab_catalog_with_type_filter(client, auth_headers):
    """Test getting prefab catalog filtered by type."""
    response = client.get("/api/v1/prefab-catalog/?prefab_type=building", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    # All returned prefabs should be of type "building"
    for prefab in data["prefabs"]:
        assert prefab["type"] == "building"


def test_get_prefab_catalog_pagination(client, auth_headers):
    """Test prefab catalog pagination."""
    response = client.get("/api/v1/prefab-catalog/?limit=2&offset=0", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["page_size"] == 2
    assert len(data["prefabs"]) <= 2


def test_get_prefab_by_id(client, auth_headers):
    """Test getting a specific prefab by ID."""
    # First get the catalog to find a prefab ID
    catalog_response = client.get("/api/v1/prefab-catalog/", headers=auth_headers)
    catalog_data = catalog_response.json()
    
    if catalog_data["prefabs"]:
        prefab_id = catalog_data["prefabs"][0]["id"]
        
        response = client.get(f"/api/v1/prefab-catalog/{prefab_id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert len(data["prefabs"]) == 1
        assert data["prefabs"][0]["id"] == prefab_id


def test_get_prefab_by_id_not_found(client, auth_headers):
    """Test getting non-existent prefab by ID."""
    response = client.get("/api/v1/prefab-catalog/non_existent_id", headers=auth_headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_search_prefabs(client, auth_headers):
    """Test searching prefabs."""
    response = client.get("/api/v1/prefab-catalog/search/?q=castle", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert "prefabs" in data
    assert isinstance(data["prefabs"], list)


def test_search_prefabs_with_type_filter(client, auth_headers):
    """Test searching prefabs with type filter."""
    response = client.get("/api/v1/prefab-catalog/search/?q=tree&prefab_type=environment", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    # All returned prefabs should be of type "environment"
    for prefab in data["prefabs"]:
        assert prefab["type"] == "environment"


def test_search_prefabs_empty_query(client, auth_headers):
    """Test searching with empty query."""
    response = client.get("/api/v1/prefab-catalog/search/?q=", headers=auth_headers)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_prefab_catalog_unauthorized(client):
    """Test accessing prefab catalog without authentication."""
    response = client.get("/api/v1/prefab-catalog/")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
