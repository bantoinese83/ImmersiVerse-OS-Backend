"""Telemetry service for tracking user events and analytics."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import TelemetryEventModel
from app.schemas import TelemetryEvent


class TelemetryService:
    """Service for handling telemetry events and analytics."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def log_event(self, event: TelemetryEvent) -> TelemetryEvent:
        """Log a telemetry event."""
        from datetime import datetime
        timestamp = datetime.fromisoformat(event.timestamp) if isinstance(event.timestamp, str) else event.timestamp
        
        event_model = TelemetryEventModel(
            id=str(event.id) if hasattr(event, 'id') else None,
            event_type=event.event_type,
            user_id=event.user_id,
            session_id=event.session_id,
            world_id=event.world_id,
            experience_id=event.experience_id,
            data=event.data,
            timestamp=timestamp
        )
        
        self.db.add(event_model)
        self.db.commit()
        self.db.refresh(event_model)
        
        return event
    
    def get_user_events(self, user_id: str, limit: int = 100) -> List[TelemetryEvent]:
        """Get telemetry events for a specific user."""
        event_models = self.db.query(TelemetryEventModel).filter(
            TelemetryEventModel.user_id == user_id
        ).order_by(TelemetryEventModel.timestamp.desc()).limit(limit).all()
        
        return [
            TelemetryEvent(
                event_type=event.event_type,
                user_id=event.user_id,
                session_id=event.session_id,
                world_id=event.world_id,
                experience_id=event.experience_id,
                data=event.data,
                timestamp=event.timestamp
            )
            for event in event_models
        ]
    
    def get_session_events(self, session_id: str) -> List[TelemetryEvent]:
        """Get telemetry events for a specific session."""
        event_models = self.db.query(TelemetryEventModel).filter(
            TelemetryEventModel.session_id == session_id
        ).order_by(TelemetryEventModel.timestamp.asc()).all()
        
        return [
            TelemetryEvent(
                event_type=event.event_type,
                user_id=event.user_id,
                session_id=event.session_id,
                world_id=event.world_id,
                experience_id=event.experience_id,
                data=event.data,
                timestamp=event.timestamp
            )
            for event in event_models
        ]
    
    def get_world_events(self, world_id: str, limit: int = 100) -> List[TelemetryEvent]:
        """Get telemetry events for a specific world."""
        event_models = self.db.query(TelemetryEventModel).filter(
            TelemetryEventModel.world_id == world_id
        ).order_by(TelemetryEventModel.timestamp.desc()).limit(limit).all()
        
        return [
            TelemetryEvent(
                event_type=event.event_type,
                user_id=event.user_id,
                session_id=event.session_id,
                world_id=event.world_id,
                experience_id=event.experience_id,
                data=event.data,
                timestamp=event.timestamp
            )
            for event in event_models
        ]
    
    def get_experience_events(self, experience_id: str, limit: int = 100) -> List[TelemetryEvent]:
        """Get telemetry events for a specific experience."""
        event_models = self.db.query(TelemetryEventModel).filter(
            TelemetryEventModel.experience_id == experience_id
        ).order_by(TelemetryEventModel.timestamp.desc()).limit(limit).all()
        
        return [
            TelemetryEvent(
                event_type=event.event_type,
                user_id=event.user_id,
                session_id=event.session_id,
                world_id=event.world_id,
                experience_id=event.experience_id,
                data=event.data,
                timestamp=event.timestamp
            )
            for event in event_models
        ]
    
    def get_event_statistics(self, event_type: str, days: int = 30) -> dict:
        """Get statistics for a specific event type over a time period."""
        from datetime import datetime, timedelta
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        events = self.db.query(TelemetryEventModel).filter(
            TelemetryEventModel.event_type == event_type,
            TelemetryEventModel.timestamp >= start_date
        ).all()
        
        return {
            "event_type": event_type,
            "total_events": len(events),
            "unique_users": len(set(event.user_id for event in events)),
            "unique_sessions": len(set(event.session_id for event in events)),
            "date_range_days": days
        }
