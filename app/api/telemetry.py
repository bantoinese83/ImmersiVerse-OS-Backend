"""Telemetry endpoint for tracking user events."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session, get_current_user_id
from app.schemas import TelemetryEvent, TelemetryResponse, ErrorResponse
from app.services.telemetry_service import TelemetryService
from app.exceptions import TelemetryError

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])


@router.post(
    "/",
    response_model=TelemetryResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def log_telemetry_event(
    event: TelemetryEvent,
    db: Session = Depends(get_database_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Log a telemetry event.
    
    This endpoint accepts telemetry events from Unity clients to track user behavior,
    performance metrics, and usage analytics.
    """
    try:
        # Initialize telemetry service
        telemetry_service = TelemetryService(db)
        
        # Log the event
        telemetry_service.log_event(event)
        
        return TelemetryResponse(
            success=True,
            message="Telemetry event logged successfully"
        )
        
    except TelemetryError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Telemetry error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/batch",
    response_model=TelemetryResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def log_telemetry_events_batch(
    events: List[TelemetryEvent],
    db: Session = Depends(get_database_session),
    user_id: str = Depends(get_current_user_id)
):
    """
    Log multiple telemetry events in a single request.
    
    This endpoint accepts a batch of telemetry events for efficient logging
    when multiple events need to be sent at once.
    """
    try:
        # Initialize telemetry service
        telemetry_service = TelemetryService(db)
        
        # Log all events
        for event in events:
            telemetry_service.log_event(event)
        
        return TelemetryResponse(
            success=True,
            message=f"Successfully logged {len(events)} telemetry events"
        )
        
    except TelemetryError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Telemetry error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/events/user/{user_id}",
    response_model=List[TelemetryEvent],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def get_user_events(
    user_id: str,
    limit: int = 100,
    db: Session = Depends(get_database_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Get telemetry events for a specific user.
    
    Returns a list of telemetry events for the specified user.
    Only the user themselves can access their own events.
    """
    try:
        # Check if user is accessing their own events
        if user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Cannot access other users' events"
            )
        
        # Initialize telemetry service
        telemetry_service = TelemetryService(db)
        
        # Get user events
        events = telemetry_service.get_user_events(user_id, limit=limit)
        
        return events
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
