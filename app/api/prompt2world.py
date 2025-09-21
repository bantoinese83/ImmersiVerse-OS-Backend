"""Prompt to world conversion endpoint."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session, get_current_user_id
from app.schemas import PromptRequest, PromptResponse, ErrorResponse
from app.services.world_generator import WorldGeneratorService
from app.exceptions import WorldGenerationError

router = APIRouter(prefix="/prompt2world", tags=["Prompt to World"])


@router.post(
    "/",
    response_model=PromptResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def convert_prompt_to_world(
    request: PromptRequest,
    db: Session = Depends(get_database_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Convert a text prompt into a structured world blueprint.
    
    This endpoint takes a text description and generates a complete world blueprint
    that can be used by Unity to instantiate a 3D world with prefabs, spawn points,
    and environment settings.
    """
    try:
        # Initialize world generator service
        world_service = WorldGeneratorService(db)
        
        # Generate world blueprint from prompt
        world_blueprint = world_service.generate_world_from_prompt(request)
        
        return PromptResponse(
            success=True,
            world_blueprint=world_blueprint,
            message="World blueprint generated successfully",
            processing_time_ms=world_blueprint.processing_time_ms
        )
        
    except WorldGenerationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"World generation failed: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
