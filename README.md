# ImmersiVerse OS Backend

A robust FastAPI backend that transforms text prompts into immersive 3D worlds for Unity integration. This backend powers the ImmersiVerse OS MVP pipeline, converting natural language descriptions into structured JSON blueprints that Unity can instantiate as interactive 3D experiences.

## 🚀 Features

- **Prompt to World Conversion**: Transform text prompts into detailed world blueprints
- **Experience Publishing**: Publish and share world experiences
- **Unity Integration**: Prefab catalog API for seamless Unity client integration
- **Telemetry & Analytics**: Comprehensive event tracking and user analytics
- **Session Management**: Secure user authentication with JWT tokens
- **RESTful API**: Clean, well-documented REST endpoints
- **Database Support**: PostgreSQL with SQLAlchemy ORM
- **Comprehensive Testing**: Unit and integration tests with 90%+ coverage

## 🏗️ Architecture

The backend follows a clean, modular architecture with clear separation of concerns:

```
app/
├── api/                    # FastAPI route handlers
│   ├── auth.py            # Authentication endpoints
│   ├── prompt2world.py    # Prompt to world conversion
│   ├── publish.py         # Experience publishing
│   ├── telemetry.py       # Analytics and telemetry
│   └── prefab_catalog.py  # Unity prefab integration
├── services/              # Business logic layer
│   ├── world_generator.py # World generation algorithms
│   ├── experience_service.py # Experience management
│   ├── prefab_service.py  # Prefab catalog management
│   ├── telemetry_service.py # Analytics processing
│   └── session_service.py # Authentication & sessions
├── schemas.py             # Pydantic data models
├── models.py              # SQLAlchemy database models
├── database.py            # Database configuration
├── config.py              # Application settings
├── exceptions.py          # Custom exceptions
├── middleware.py          # Custom middleware
└── main.py               # FastAPI application
```

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis 6+ (optional, for caching)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bantoinese83/ImmersiVerse-OS-Backend.git
   cd fastapi-json-blueprint
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb immersiverse

   # Run migrations
   alembic upgrade head
   ```

6. **Seed default data**
   ```bash
   python -m app.services.prefab_service  # Seeds prefab catalog
   ```

## 🚀 Quick Start

1. **Start the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Test the API**
   ```bash
   # Create a session
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
        -H "Content-Type: application/json" \
        -d '{"user_id": "test_user"}'

   # Convert a prompt to world
   curl -X POST "http://localhost:8000/api/v1/prompt2world/" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer YOUR_TOKEN" \
        -d '{
          "prompt": "A magical forest with ancient trees and glowing mushrooms",
          "world_type": "fantasy",
          "user_id": "test_user"
        }'
   ```

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Create user session
- `POST /api/v1/auth/logout` - Invalidate session
- `GET /api/v1/auth/validate` - Validate session token

### World Generation
- `POST /api/v1/prompt2world/` - Convert text prompt to world blueprint

### Experience Publishing
- `POST /api/v1/publish/` - Publish world as experience
- `GET /api/v1/publish/experiences` - List public experiences
- `GET /api/v1/publish/experiences/{id}` - Get specific experience

### Telemetry & Analytics
- `POST /api/v1/telemetry/` - Log single telemetry event
- `POST /api/v1/telemetry/batch` - Log multiple events
- `GET /api/v1/telemetry/events/user/{user_id}` - Get user events

### Unity Integration
- `GET /api/v1/prefab-catalog/` - Get prefab catalog
- `GET /api/v1/prefab-catalog/{id}` - Get specific prefab
- `GET /api/v1/prefab-catalog/search` - Search prefabs

## 🎮 Unity Integration

The backend provides a comprehensive prefab catalog API that Unity clients can use to:

1. **Fetch Available Prefabs**
   ```csharp
   // Unity C# example
   var response = await client.GetAsync("/api/v1/prefab-catalog/");
   var catalog = JsonUtility.FromJson<PrefabCatalogResponse>(response);
   ```

2. **Download and Instantiate Prefabs**
   ```csharp
   // Download prefab from download_url
   // Instantiate using Unity's Instantiate method
   var prefab = Resources.Load<GameObject>(prefabId);
   var instance = Instantiate(prefab, position, rotation);
   ```

3. **Apply World Blueprint**
   ```csharp
   // Parse world blueprint JSON
   var blueprint = JsonUtility.FromJson<WorldBlueprint>(blueprintJson);
   
   // Instantiate all prefab instances
   foreach (var prefabInstance in blueprint.prefabInstances)
   {
       var prefab = GetPrefabById(prefabInstance.prefabId);
       var instance = Instantiate(prefab, prefabInstance.position, prefabInstance.rotation);
       instance.transform.localScale = prefabInstance.scale;
   }
   ```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_prompt2world.py

# Run with verbose output
pytest -v
```

## 📊 Data Models

### WorldBlueprint
```json
{
  "id": "uuid",
  "prompt": "A magical forest with ancient trees",
  "world_type": "fantasy",
  "title": "Magical Forest World",
  "description": "A mystical forest filled with wonder...",
  "environment_settings": {
    "lighting": "mystical",
    "weather": "ethereal"
  },
  "prefab_instances": [
    {
      "id": "uuid",
      "prefab_id": "magic_tree_01",
      "prefab_type": "environment",
      "position": {"x": 0, "y": 0, "z": 0},
      "rotation": {"x": 0, "y": 0, "z": 0, "w": 1},
      "scale": {"x": 1, "y": 1, "z": 1},
      "properties": {}
    }
  ],
  "spawn_points": [
    {"x": 0, "y": 1, "z": 0}
  ]
}
```

### ExperienceCard
```json
{
  "id": "uuid",
  "world_blueprint_id": "uuid",
  "title": "Magical Forest Experience",
  "description": "Explore a mystical forest...",
  "thumbnail_url": "https://example.com/thumb.jpg",
  "tags": ["fantasy", "forest", "magic"],
  "author_id": "user123",
  "is_public": true,
  "play_count": 42,
  "rating": 4.5
}
```

## 🔧 Configuration

Environment variables (see `.env.example`):

```bash
# Application
APP_NAME="ImmersiVerse OS Backend"
DEBUG=false
API_V1_PREFIX="/api/v1"

# Database
DATABASE_URL="postgresql://user:password@localhost/immersiverse"
DATABASE_ECHO=false

# Redis
REDIS_URL="redis://localhost:6379"

# Security
SECRET_KEY="your-secret-key-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

1. **Environment Variables**: Set all production environment variables
2. **Database**: Use managed PostgreSQL service (AWS RDS, Google Cloud SQL)
3. **Redis**: Use managed Redis service for caching
4. **Security**: Use strong secret keys and enable HTTPS
5. **Monitoring**: Set up logging and monitoring (Sentry, DataDog)
6. **Scaling**: Use load balancers and horizontal scaling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the API documentation at `/docs`

## 🔮 Roadmap

- [ ] Machine Learning integration for better world generation
- [ ] Real-time collaboration features
- [ ] Advanced prefab customization
- [ ] Performance optimization
- [ ] Mobile API support
- [ ] WebSocket support for real-time updates

---

**Built with ❤️ for ImmersiVerse OS**
