"""Experience publishing and management service."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import ExperienceCardModel, WorldBlueprintModel
from app.schemas import ExperienceCard, PublishRequest


class ExperienceService:
    """Service for managing experience cards and publishing."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def publish_experience(self, request: PublishRequest) -> ExperienceCard:
        """Publish a world blueprint as an experience."""
        # Verify world blueprint exists
        world_blueprint = self.db.query(WorldBlueprintModel).filter(
            WorldBlueprintModel.id == request.world_blueprint_id
        ).first()
        
        if not world_blueprint:
            raise ValueError(f"World blueprint {request.world_blueprint_id} not found")
        
        # Create experience card
        experience_model = ExperienceCardModel(
            world_blueprint_id=request.world_blueprint_id,
            title=request.title,
            description=request.description,
            tags=request.tags,
            author_id=request.user_id,
            is_public=request.is_public
        )
        
        self.db.add(experience_model)
        self.db.commit()
        self.db.refresh(experience_model)
        
        return ExperienceCard(
            id=experience_model.id,
            world_blueprint_id=experience_model.world_blueprint_id,
            title=experience_model.title,
            description=experience_model.description,
            thumbnail_url=experience_model.thumbnail_url,
            tags=experience_model.tags,
            author_id=experience_model.author_id,
            is_public=experience_model.is_public,
            play_count=experience_model.play_count,
            rating=experience_model.rating,
            created_at=experience_model.created_at,
            updated_at=experience_model.updated_at
        )
    
    def get_experience_by_id(self, experience_id: str) -> Optional[ExperienceCard]:
        """Get an experience by ID."""
        experience_model = self.db.query(ExperienceCardModel).filter(
            ExperienceCardModel.id == experience_id
        ).first()
        
        if not experience_model:
            return None
        
        return ExperienceCard(
            id=experience_model.id,
            world_blueprint_id=experience_model.world_blueprint_id,
            title=experience_model.title,
            description=experience_model.description,
            thumbnail_url=experience_model.thumbnail_url,
            tags=experience_model.tags,
            author_id=experience_model.author_id,
            is_public=experience_model.is_public,
            play_count=experience_model.play_count,
            rating=experience_model.rating,
            created_at=experience_model.created_at,
            updated_at=experience_model.updated_at
        )
    
    def get_public_experiences(self, limit: int = 20, offset: int = 0) -> List[ExperienceCard]:
        """Get public experiences with pagination."""
        experience_models = self.db.query(ExperienceCardModel).filter(
            ExperienceCardModel.is_public == True
        ).offset(offset).limit(limit).all()
        
        return [
            ExperienceCard(
                id=exp.id,
                world_blueprint_id=exp.world_blueprint_id,
                title=exp.title,
                description=exp.description,
                thumbnail_url=exp.thumbnail_url,
                tags=exp.tags,
                author_id=exp.author_id,
                is_public=exp.is_public,
                play_count=exp.play_count,
                rating=exp.rating,
                created_at=exp.created_at,
                updated_at=exp.updated_at
            )
            for exp in experience_models
        ]
    
    def get_user_experiences(self, user_id: str, limit: int = 20, offset: int = 0) -> List[ExperienceCard]:
        """Get experiences created by a specific user."""
        experience_models = self.db.query(ExperienceCardModel).filter(
            ExperienceCardModel.author_id == user_id
        ).offset(offset).limit(limit).all()
        
        return [
            ExperienceCard(
                id=exp.id,
                world_blueprint_id=exp.world_blueprint_id,
                title=exp.title,
                description=exp.description,
                thumbnail_url=exp.thumbnail_url,
                tags=exp.tags,
                author_id=exp.author_id,
                is_public=exp.is_public,
                play_count=exp.play_count,
                rating=exp.rating,
                created_at=exp.created_at,
                updated_at=exp.updated_at
            )
            for exp in experience_models
        ]
    
    def increment_play_count(self, experience_id: str) -> bool:
        """Increment the play count for an experience."""
        experience_model = self.db.query(ExperienceCardModel).filter(
            ExperienceCardModel.id == experience_id
        ).first()
        
        if not experience_model:
            return False
        
        experience_model.play_count += 1
        self.db.commit()
        return True
    
    def update_rating(self, experience_id: str, rating: float) -> bool:
        """Update the rating for an experience."""
        if not 0.0 <= rating <= 5.0:
            raise ValueError("Rating must be between 0.0 and 5.0")
        
        experience_model = self.db.query(ExperienceCardModel).filter(
            ExperienceCardModel.id == experience_id
        ).first()
        
        if not experience_model:
            return False
        
        experience_model.rating = rating
        self.db.commit()
        return True
