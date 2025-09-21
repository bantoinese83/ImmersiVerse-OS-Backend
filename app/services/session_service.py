"""User session management service."""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.models import UserSessionModel
from app.schemas import UserSession

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SessionService:
    """Service for managing user sessions and authentication."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_access_token(self, user_id: str, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token for a user."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        to_encode = {"sub": user_id, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    
    def create_session(self, user_id: str) -> UserSession:
        """Create a new user session."""
        # Create JWT token
        token = self.create_access_token(user_id)
        
        # Create session record
        session_model = UserSessionModel(
            user_id=user_id,
            session_id=str(uuid.uuid4()),
            token=token,
            expires_at=datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        )
        
        self.db.add(session_model)
        self.db.commit()
        self.db.refresh(session_model)
        
        return UserSession(
            user_id=session_model.user_id,
            session_id=session_model.session_id,
            token=session_model.token,
            expires_at=session_model.expires_at,
            created_at=session_model.created_at
        )
    
    def validate_token(self, token: str) -> Optional[str]:
        """Validate a JWT token and return the user ID."""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return user_id
        except JWTError:
            return None
    
    def get_session_by_token(self, token: str) -> Optional[UserSessionModel]:
        """Get session by token."""
        return self.db.query(UserSessionModel).filter(
            UserSessionModel.token == token,
            UserSessionModel.is_active == True,
            UserSessionModel.expires_at > datetime.utcnow()
        ).first()
    
    def invalidate_session(self, token: str) -> bool:
        """Invalidate a session by token."""
        session = self.get_session_by_token(token)
        if session:
            session.is_active = False
            self.db.commit()
            return True
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions and return count of cleaned sessions."""
        expired_sessions = self.db.query(UserSessionModel).filter(
            UserSessionModel.expires_at < datetime.utcnow()
        ).all()
        
        count = len(expired_sessions)
        for session in expired_sessions:
            session.is_active = False
        
        self.db.commit()
        return count


# Import uuid at the top level
import uuid
