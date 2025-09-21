"""Dependencies for API endpoints."""

from typing import Optional

from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.database import get_database_session
from app.services.session_service import SessionService
from app.exceptions import AuthenticationError


def get_session_service(db: Session = Depends(get_database_session)) -> SessionService:
    """Get session service dependency."""
    return SessionService(db)


def get_current_user_id(
    authorization: Optional[str] = Header(None),
    session_service: SessionService = Depends(get_session_service)
) -> str:
    """Get current user ID from authorization header."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    # Extract token from "Bearer <token>" format
    try:
        scheme, token = authorization.split(" ", 1)
        if scheme.lower() != "bearer":
            raise ValueError("Invalid authorization scheme")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    
    # Validate token
    user_id = session_service.validate_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return user_id
