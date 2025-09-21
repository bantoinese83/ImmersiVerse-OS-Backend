"""Experience publishing endpoint."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session, get_current_user_id
from app.schemas import PublishRequest, PublishResponse, ErrorResponse
from app.services.experience_service import ExperienceService
from app.exceptions import ValidationError, NotFoundError

router = APIRouter(prefix="/publish", tags=["Publishing"])


@router.post(
    "/",
    response_model=PublishResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def publish_experience(
    request: PublishRequest,
    db: Session = Depends(get_database_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Publish a world blueprint as a public experience.
    
    This endpoint takes a world blueprint ID and creates a public experience card
    that can be discovered and played by other users.
    """
    try:
        # Initialize experience service
        experience_service = ExperienceService(db)
        
        # Publish the experience
        experience_card = experience_service.publish_experience(request)
        
        return PublishResponse(
            success=True,
            experience_card=experience_card,
            message="Experience published successfully"
        )
        
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/experiences",
    response_model=List[PublishResponse],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def get_public_experiences(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_database_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Get list of public experiences.
    
    Returns a paginated list of publicly available experiences that users can play.
    """
    try:
        experience_service = ExperienceService(db)
        experiences = experience_service.get_public_experiences(limit=limit, offset=offset)
        
        return [
            PublishResponse(
                success=True,
                experience_card=exp,
                message="Experience retrieved successfully"
            )
            for exp in experiences
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/experiences/{experience_id}",
    response_model=PublishResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def get_experience_by_id(
    experience_id: str,
    db: Session = Depends(get_database_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Get a specific experience by ID.
    
    Returns the details of a specific experience including its world blueprint.
    """
    try:
        experience_service = ExperienceService(db)
        experience = experience_service.get_experience_by_id(experience_id)
        
        if not experience:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Experience {experience_id} not found"
            )
        
        return PublishResponse(
            success=True,
            experience_card=experience,
            message="Experience retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
