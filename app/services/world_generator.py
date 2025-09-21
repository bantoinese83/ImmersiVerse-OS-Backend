"""World generation service for converting prompts to world blueprints."""

import time
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import WorldBlueprintModel
from app.schemas import WorldBlueprint, WorldType, PrefabInstance, PrefabType, Vector3, Quaternion, PromptRequest


class WorldGeneratorService:
    """Service for generating world blueprints from text prompts."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_world_from_prompt(self, request: PromptRequest) -> WorldBlueprint:
        """Generate a world blueprint from a text prompt."""
        start_time = time.time()
        
        # Determine world type if not specified
        world_type = request.world_type or self._infer_world_type(request.prompt)
        
        # Generate world blueprint
        world_blueprint = self._create_world_blueprint(request.prompt, world_type)
        
        # Save to database
        world_model = WorldBlueprintModel(
            id=world_blueprint.id,
            prompt=world_blueprint.prompt,
            world_type=world_blueprint.world_type.value,
            title=world_blueprint.title,
            description=world_blueprint.description,
            environment_settings=world_blueprint.environment_settings,
            prefab_instances=[instance.model_dump() for instance in world_blueprint.prefab_instances],
            spawn_points=[point.model_dump() for point in world_blueprint.spawn_points]
        )
        
        self.db.add(world_model)
        self.db.commit()
        
        processing_time = int((time.time() - start_time) * 1000)
        world_blueprint.processing_time_ms = processing_time
        
        return world_blueprint
    
    def _infer_world_type(self, prompt: str) -> WorldType:
        """Infer world type from prompt content."""
        prompt_lower = prompt.lower()
        
        # Simple keyword-based inference (in production, use ML/NLP)
        if any(word in prompt_lower for word in ["fantasy", "magic", "dragon", "wizard", "castle"]):
            return WorldType.FANTASY
        elif any(word in prompt_lower for word in ["space", "alien", "robot", "future", "sci-fi"]):
            return WorldType.SCI_FI
        elif any(word in prompt_lower for word in ["city", "urban", "street", "building"]):
            return WorldType.URBAN
        elif any(word in prompt_lower for word in ["forest", "mountain", "nature", "wilderness"]):
            return WorldType.NATURE
        elif any(word in prompt_lower for word in ["medieval", "ancient", "historical", "vintage"]):
            return WorldType.HISTORICAL
        else:
            return WorldType.REALISTIC
    
    def _create_world_blueprint(self, prompt: str, world_type: WorldType) -> WorldBlueprint:
        """Create a world blueprint based on prompt and type."""
        # Generate title and description
        title = self._generate_title(prompt, world_type)
        description = self._generate_description(prompt, world_type)
        
        # Generate environment settings
        environment_settings = self._generate_environment_settings(world_type)
        
        # Generate prefab instances
        prefab_instances = self._generate_prefab_instances(prompt, world_type)
        
        # Generate spawn points
        spawn_points = self._generate_spawn_points(world_type)
        
        return WorldBlueprint(
            prompt=prompt,
            world_type=world_type,
            title=title,
            description=description,
            environment_settings=environment_settings,
            prefab_instances=prefab_instances,
            spawn_points=spawn_points
        )
    
    def _generate_title(self, prompt: str, world_type: WorldType) -> str:
        """Generate a title for the world."""
        # Simple title generation (in production, use more sophisticated NLP)
        words = prompt.split()[:5]  # Take first 5 words
        title = " ".join(words).title()
        return f"{title} World"
    
    def _generate_description(self, prompt: str, world_type: WorldType) -> str:
        """Generate a description for the world."""
        # Simple description generation (in production, use more sophisticated NLP)
        base_descriptions = {
            WorldType.FANTASY: "A magical realm filled with wonder and enchantment.",
            WorldType.SCI_FI: "A futuristic world with advanced technology and alien landscapes.",
            WorldType.REALISTIC: "A realistic environment based on real-world locations.",
            WorldType.SURREAL: "A dreamlike world that defies conventional reality.",
            WorldType.HISTORICAL: "A historical setting that captures the essence of the past.",
            WorldType.URBAN: "A bustling urban environment with modern architecture.",
            WorldType.NATURE: "A natural environment filled with organic beauty.",
            WorldType.SPACE: "An otherworldly space environment with cosmic wonders."
        }
        
        return f"Generated from: '{prompt}'. {base_descriptions.get(world_type, 'A unique world to explore.')}"
    
    def _generate_environment_settings(self, world_type: WorldType) -> dict:
        """Generate environment settings based on world type."""
        settings_templates = {
            WorldType.FANTASY: {
                "lighting": "mystical",
                "weather": "ethereal",
                "ambient_sound": "magical_forest",
                "skybox": "fantasy_sky"
            },
            WorldType.SCI_FI: {
                "lighting": "neon",
                "weather": "none",
                "ambient_sound": "space_station",
                "skybox": "space_stars"
            },
            WorldType.REALISTIC: {
                "lighting": "natural",
                "weather": "clear",
                "ambient_sound": "city_traffic",
                "skybox": "realistic_sky"
            },
            WorldType.URBAN: {
                "lighting": "street_lights",
                "weather": "overcast",
                "ambient_sound": "urban_bustle",
                "skybox": "city_skyline"
            },
            WorldType.NATURE: {
                "lighting": "sunlight",
                "weather": "sunny",
                "ambient_sound": "birds_chirping",
                "skybox": "forest_canopy"
            }
        }
        
        return settings_templates.get(world_type, settings_templates[WorldType.REALISTIC])
    
    def _generate_prefab_instances(self, prompt: str, world_type: WorldType) -> List[PrefabInstance]:
        """Generate prefab instances based on prompt and world type."""
        instances = []
        
        # Generate basic environment prefabs
        if world_type == WorldType.FANTASY:
            instances.extend([
                PrefabInstance(
                    prefab_id="fantasy_castle_01",
                    prefab_type=PrefabType.BUILDING,
                    position=Vector3(x=0, y=0, z=0),
                    rotation=Quaternion(x=0, y=0, z=0, w=1),
                    properties={"theme": "medieval", "size": "large"}
                ),
                PrefabInstance(
                    prefab_id="magic_tree_01",
                    prefab_type=PrefabType.ENVIRONMENT,
                    position=Vector3(x=10, y=0, z=5),
                    rotation=Quaternion(x=0, y=0, z=0, w=1),
                    properties={"glow": True, "animated": True}
                )
            ])
        elif world_type == WorldType.SCI_FI:
            instances.extend([
                PrefabInstance(
                    prefab_id="space_station_01",
                    prefab_type=PrefabType.BUILDING,
                    position=Vector3(x=0, y=0, z=0),
                    rotation=Quaternion(x=0, y=0, z=0, w=1),
                    properties={"theme": "futuristic", "size": "massive"}
                ),
                PrefabInstance(
                    prefab_id="hologram_display_01",
                    prefab_type=PrefabType.UI,
                    position=Vector3(x=5, y=2, z=0),
                    rotation=Quaternion(x=0, y=0, z=0, w=1),
                    properties={"interactive": True, "glow": True}
                )
            ])
        else:
            # Default realistic environment
            instances.extend([
                PrefabInstance(
                    prefab_id="modern_building_01",
                    prefab_type=PrefabType.BUILDING,
                    position=Vector3(x=0, y=0, z=0),
                    rotation=Quaternion(x=0, y=0, z=0, w=1),
                    properties={"theme": "modern", "size": "medium"}
                )
            ])
        
        return instances
    
    def _generate_spawn_points(self, world_type: WorldType) -> List[Vector3]:
        """Generate spawn points for the world."""
        if world_type == WorldType.FANTASY:
            return [
                Vector3(x=0, y=1, z=0),  # In front of castle
                Vector3(x=10, y=1, z=5)  # Near magic tree
            ]
        elif world_type == WorldType.SCI_FI:
            return [
                Vector3(x=0, y=1, z=0),  # In space station
                Vector3(x=5, y=1, z=0)   # Near hologram
            ]
        else:
            return [
                Vector3(x=0, y=1, z=0),  # Default spawn
                Vector3(x=5, y=1, z=5)   # Secondary spawn
            ]
