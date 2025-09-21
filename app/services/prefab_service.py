"""Prefab catalog service for Unity integration."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import PrefabCatalogModel
from app.schemas import PrefabCatalogItem, PrefabType


class PrefabService:
    """Service for managing prefab catalog and Unity integration."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_prefab_catalog(self, prefab_type: Optional[PrefabType] = None, 
                          limit: int = 50, offset: int = 0) -> List[PrefabCatalogItem]:
        """Get prefab catalog items with optional filtering."""
        query = self.db.query(PrefabCatalogModel)
        
        if prefab_type:
            query = query.filter(PrefabCatalogModel.type == prefab_type.value)
        
        prefab_models = query.offset(offset).limit(limit).all()
        
        return [
            PrefabCatalogItem(
                id=prefab.id,
                name=prefab.name,
                type=PrefabType(prefab.type),
                description=prefab.description,
                thumbnail_url=prefab.thumbnail_url,
                download_url=prefab.download_url,
                size_bytes=prefab.size_bytes,
                version=prefab.version,
                tags=prefab.tags,
                properties=prefab.properties
            )
            for prefab in prefab_models
        ]
    
    def get_prefab_by_id(self, prefab_id: str) -> Optional[PrefabCatalogItem]:
        """Get a specific prefab by ID."""
        prefab_model = self.db.query(PrefabCatalogModel).filter(
            PrefabCatalogModel.id == prefab_id
        ).first()
        
        if not prefab_model:
            return None
        
        return PrefabCatalogItem(
            id=prefab_model.id,
            name=prefab_model.name,
            type=PrefabType(prefab_model.type),
            description=prefab_model.description,
            thumbnail_url=prefab_model.thumbnail_url,
            download_url=prefab_model.download_url,
            size_bytes=prefab_model.size_bytes,
            version=prefab_model.version,
            tags=prefab_model.tags,
            properties=prefab_model.properties
        )
    
    def search_prefabs(self, query: str, prefab_type: Optional[PrefabType] = None,
                      limit: int = 20) -> List[PrefabCatalogItem]:
        """Search prefabs by name, description, or tags."""
        db_query = self.db.query(PrefabCatalogModel).filter(
            PrefabCatalogModel.name.ilike(f"%{query}%") |
            PrefabCatalogModel.description.ilike(f"%{query}%")
        )
        
        if prefab_type:
            db_query = db_query.filter(PrefabCatalogModel.type == prefab_type.value)
        
        prefab_models = db_query.limit(limit).all()
        
        return [
            PrefabCatalogItem(
                id=prefab.id,
                name=prefab.name,
                type=PrefabType(prefab.type),
                description=prefab.description,
                thumbnail_url=prefab.thumbnail_url,
                download_url=prefab.download_url,
                size_bytes=prefab.size_bytes,
                version=prefab.version,
                tags=prefab.tags,
                properties=prefab.properties
            )
            for prefab in prefab_models
        ]
    
    def add_prefab_to_catalog(self, prefab_item: PrefabCatalogItem) -> PrefabCatalogItem:
        """Add a new prefab to the catalog."""
        prefab_model = PrefabCatalogModel(
            id=prefab_item.id,
            name=prefab_item.name,
            type=prefab_item.type.value,
            description=prefab_item.description,
            thumbnail_url=prefab_item.thumbnail_url,
            download_url=prefab_item.download_url,
            size_bytes=prefab_item.size_bytes,
            version=prefab_item.version,
            tags=prefab_item.tags,
            properties=prefab_item.properties
        )
        
        self.db.add(prefab_model)
        self.db.commit()
        self.db.refresh(prefab_model)
        
        return prefab_item
    
    def get_total_prefab_count(self, prefab_type: Optional[PrefabType] = None) -> int:
        """Get total count of prefabs in catalog."""
        query = self.db.query(PrefabCatalogModel)
        
        if prefab_type:
            query = query.filter(PrefabCatalogModel.type == prefab_type.value)
        
        return query.count()
    
    def seed_default_prefabs(self) -> None:
        """Seed the database with default prefab catalog items."""
        default_prefabs = [
            PrefabCatalogItem(
                id="fantasy_castle_01",
                name="Medieval Castle",
                type=PrefabType.BUILDING,
                description="A grand medieval castle with towers and battlements",
                download_url="https://example.com/prefabs/fantasy_castle_01.unitypackage",
                size_bytes=1024000,
                version="1.0.0",
                tags=["fantasy", "medieval", "castle", "building"],
                properties={"poly_count": 5000, "textures": 8, "materials": 3}
            ),
            PrefabCatalogItem(
                id="space_station_01",
                name="Space Station Alpha",
                type=PrefabType.BUILDING,
                description="A futuristic space station with docking bays",
                download_url="https://example.com/prefabs/space_station_01.unitypackage",
                size_bytes=2048000,
                version="1.0.0",
                tags=["sci-fi", "space", "station", "building"],
                properties={"poly_count": 8000, "textures": 12, "materials": 5}
            ),
            PrefabCatalogItem(
                id="magic_tree_01",
                name="Enchanted Tree",
                type=PrefabType.ENVIRONMENT,
                description="A mystical tree with glowing leaves and magical aura",
                download_url="https://example.com/prefabs/magic_tree_01.unitypackage",
                size_bytes=512000,
                version="1.0.0",
                tags=["fantasy", "nature", "magic", "environment"],
                properties={"poly_count": 2000, "animated": True, "glow_effect": True}
            ),
            PrefabCatalogItem(
                id="hologram_display_01",
                name="Holographic Display",
                type=PrefabType.UI,
                description="A futuristic holographic interface display",
                download_url="https://example.com/prefabs/hologram_display_01.unitypackage",
                size_bytes=256000,
                version="1.0.0",
                tags=["sci-fi", "ui", "hologram", "display"],
                properties={"interactive": True, "glow_effect": True, "animated": True}
            ),
            PrefabCatalogItem(
                id="modern_building_01",
                name="Modern Office Building",
                type=PrefabType.BUILDING,
                description="A sleek modern office building with glass facade",
                download_url="https://example.com/prefabs/modern_building_01.unitypackage",
                size_bytes=1536000,
                version="1.0.0",
                tags=["modern", "urban", "building", "office"],
                properties={"poly_count": 6000, "textures": 10, "materials": 4}
            )
        ]
        
        for prefab in default_prefabs:
            # Check if prefab already exists
            existing = self.db.query(PrefabCatalogModel).filter(
                PrefabCatalogModel.id == prefab.id
            ).first()
            
            if not existing:
                self.add_prefab_to_catalog(prefab)
