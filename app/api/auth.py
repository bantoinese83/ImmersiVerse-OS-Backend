"""Authentication endpoints for user sessions."""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session, get_session_service
from app.schemas import UserSession, ErrorResponse
from app.services.session_service import SessionService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=UserSession,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def create_session(
    request: dict,
    session_service: SessionService = Depends(get_session_service)
):
    """
    Create a new user session.
    
    This endpoint creates a new session for a user and returns a session token.
    For MVP purposes, this uses stub authentication - any user_id will work.
    """
    try:
        user_id = request.get("user_id")
        if not user_id or len(user_id.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID is required"
            )
        
        # Create new session
        session = session_service.create_session(user_id.strip())
        
        return session
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {str(e)}"
        )


@router.post(
    "/logout",
    response_model=dict,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def logout_session(
    authorization: str = Header(None),
    session_service: SessionService = Depends(get_session_service)
):
    """
    Logout and invalidate a user session.
    
    This endpoint invalidates the current session token.
    """
    try:
        # Extract token from authorization header
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid authorization header format"
            )
        
        token = authorization.split(" ", 1)[1]
        
        # Invalidate session
        success = session_service.invalidate_session(token)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        return {"success": True, "message": "Session invalidated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to logout: {str(e)}"
        )


@router.get(
    "/validate",
    response_model=dict,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def validate_session(
    authorization: str = Header(None),
    session_service: SessionService = Depends(get_session_service)
):
    """
    Validate a session token.
    
    This endpoint checks if a session token is valid and returns user information.
    """
    try:
        # Extract token from authorization header
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format"
            )
        
        token = authorization.split(" ", 1)[1]
        
        # Validate token
        user_id = session_service.validate_token(token)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        # Get session details
        session = session_service.get_session_by_token(token)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session not found"
            )
        
        return {
            "valid": True,
            "user_id": user_id,
            "session_id": session.session_id,
            "expires_at": session.expires_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to validate session: {str(e)}"
        )
