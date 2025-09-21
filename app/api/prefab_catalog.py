"""Prefab catalog endpoint for Unity integration."""

from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session, get_current_user_id
from app.schemas import PrefabCatalogResponse, PrefabType, ErrorResponse
from app.services.prefab_service import PrefabService
from app.exceptions import PrefabCatalogError

router = APIRouter(prefix="/prefab-catalog", tags=["Prefab Catalog"])


@router.get(
    "/",
    response_model=PrefabCatalogResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def get_prefab_catalog(
    prefab_type: Optional[PrefabType] = Query(None, description="Filter by prefab type"),
    limit: int = Query(50, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    db: Session = Depends(get_database_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Get the Unity prefab catalog.
    
    Returns a paginated list of available prefabs that can be instantiated
    in Unity worlds. Supports filtering by prefab type.
    """
    try:
        # Initialize prefab service
        prefab_service = PrefabService(db)
        
        # Get prefab catalog
        prefabs = prefab_service.get_prefab_catalog(
            prefab_type=prefab_type,
            limit=limit,
            offset=offset
        )
        
        # Get total count
        total_count = prefab_service.get_total_prefab_count(prefab_type=prefab_type)
        
        return PrefabCatalogResponse(
            success=True,
            prefabs=prefabs,
            total_count=total_count,
            page=offset // limit + 1,
            page_size=limit
        )
        
    except PrefabCatalogError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Prefab catalog error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/{prefab_id}",
    response_model=PrefabCatalogResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def get_prefab_by_id(
    prefab_id: str,
    db: Session = Depends(get_database_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Get a specific prefab by ID.
    
    Returns detailed information about a specific prefab including
    download URL, properties, and metadata.
    """
    try:
        # Initialize prefab service
        prefab_service = PrefabService(db)
        
        # Get prefab by ID
        prefab = prefab_service.get_prefab_by_id(prefab_id)
        
        if not prefab:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prefab {prefab_id} not found"
            )
        
        return PrefabCatalogResponse(
            success=True,
            prefabs=[prefab],
            total_count=1,
            page=1,
            page_size=1
        )
        
    except HTTPException:
        raise
    except PrefabCatalogError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Prefab catalog error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/search/",
    response_model=PrefabCatalogResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def search_prefabs(
    q: str = Query(..., min_length=1, max_length=100, description="Search query"),
    prefab_type: Optional[PrefabType] = Query(None, description="Filter by prefab type"),
    limit: int = Query(20, ge=1, le=50, description="Number of results to return"),
    db: Session = Depends(get_database_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Search prefabs by name, description, or tags.
    
    Returns prefabs that match the search query in their name,
    description, or tags.
    """
    try:
        # Initialize prefab service
        prefab_service = PrefabService(db)
        
        # Search prefabs
        prefabs = prefab_service.search_prefabs(
            query=q,
            prefab_type=prefab_type,
            limit=limit
        )
        
        return PrefabCatalogResponse(
            success=True,
            prefabs=prefabs,
            total_count=len(prefabs),
            page=1,
            page_size=len(prefabs)
        )
        
    except PrefabCatalogError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Prefab catalog error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
