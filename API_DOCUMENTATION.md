# ImmersiVerse OS Backend API Documentation

## Overview

The ImmersiVerse OS Backend provides a comprehensive REST API for transforming text prompts into immersive 3D worlds. The API is built with FastAPI and follows RESTful principles with clear, consistent endpoints.

**Base URL**: `http://localhost:8000`  
**API Version**: `v1`  
**Content Type**: `application/json`

## Authentication

All endpoints (except health checks) require authentication via JWT tokens in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Getting a Token

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "user_id": "your_user_id"
}
```

**Response:**
```json
{
  "user_id": "your_user_id",
  "session_id": "uuid",
  "token": "jwt_token_here",
  "expires_at": "2024-01-01T12:00:00Z",
  "created_at": "2024-01-01T11:30:00Z"
}
```

## Core Endpoints

### 1. Prompt to World Conversion

Convert text prompts into structured world blueprints.

#### `POST /api/v1/prompt2world/`

**Request Body:**
```json
{
  "prompt": "A magical forest with ancient trees and glowing mushrooms",
  "world_type": "fantasy",
  "user_id": "user123"
}
```

**Parameters:**
- `prompt` (string, required): Text description of the desired world (1-1000 characters)
- `world_type` (string, optional): Type of world to generate (`fantasy`, `sci_fi`, `realistic`, `surreal`, `historical`, `urban`, `nature`, `space`)
- `user_id` (string, required): ID of the user making the request

**Response:**
```json
{
  "success": true,
  "world_blueprint": {
    "id": "uuid",
    "prompt": "A magical forest with ancient trees and glowing mushrooms",
    "world_type": "fantasy",
    "title": "Magical Forest World",
    "description": "A mystical forest filled with wonder and enchantment...",
    "environment_settings": {
      "lighting": "mystical",
      "weather": "ethereal",
      "ambient_sound": "magical_forest",
      "skybox": "fantasy_sky"
    },
    "prefab_instances": [
      {
        "id": "uuid",
        "prefab_id": "magic_tree_01",
        "prefab_type": "environment",
        "position": {"x": 0, "y": 0, "z": 0},
        "rotation": {"x": 0, "y": 0, "z": 0, "w": 1},
        "scale": {"x": 1, "y": 1, "z": 1},
        "properties": {"glow": true, "animated": true}
      }
    ],
    "spawn_points": [
      {"x": 0, "y": 1, "z": 0}
    ],
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  },
  "message": "World blueprint generated successfully",
  "processing_time_ms": 150
}
```

### 2. Experience Publishing

Publish world blueprints as shareable experiences.

#### `POST /api/v1/publish/`

**Request Body:**
```json
{
  "world_blueprint_id": "uuid",
  "title": "Magical Forest Experience",
  "description": "Explore a mystical forest filled with ancient trees",
  "tags": ["fantasy", "forest", "magic"],
  "is_public": true,
  "user_id": "user123"
}
```

**Response:**
```json
{
  "success": true,
  "experience_card": {
    "id": "uuid",
    "world_blueprint_id": "uuid",
    "title": "Magical Forest Experience",
    "description": "Explore a mystical forest filled with ancient trees",
    "thumbnail_url": null,
    "tags": ["fantasy", "forest", "magic"],
    "author_id": "user123",
    "is_public": true,
    "play_count": 0,
    "rating": null,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  },
  "message": "Experience published successfully"
}
```

#### `GET /api/v1/publish/experiences`

Get list of public experiences with pagination.

**Query Parameters:**
- `limit` (integer, optional): Number of items per page (default: 20, max: 100)
- `offset` (integer, optional): Number of items to skip (default: 0)

**Response:**
```json
[
  {
    "success": true,
    "experience_card": {
      "id": "uuid",
      "title": "Magical Forest Experience",
      "description": "Explore a mystical forest...",
      "author_id": "user123",
      "play_count": 42,
      "rating": 4.5,
      "created_at": "2024-01-01T12:00:00Z"
    },
    "message": "Experience retrieved successfully"
  }
]
```

### 3. Telemetry & Analytics

Track user behavior and system performance.

#### `POST /api/v1/telemetry/`

Log a single telemetry event.

**Request Body:**
```json
{
  "event_type": "world_entered",
  "user_id": "user123",
  "session_id": "session456",
  "world_id": "world789",
  "experience_id": "exp123",
  "data": {
    "action": "enter",
    "timestamp": "2024-01-01T12:00:00Z",
    "device_info": {
      "platform": "Windows",
      "unity_version": "2022.3.0f1"
    }
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Telemetry event logged successfully"
}
```

#### `POST /api/v1/telemetry/batch`

Log multiple telemetry events in a single request.

**Request Body:**
```json
[
  {
    "event_type": "world_entered",
    "user_id": "user123",
    "session_id": "session456",
    "world_id": "world789",
    "data": {"action": "enter"}
  },
  {
    "event_type": "prefab_instantiated",
    "user_id": "user123",
    "session_id": "session456",
    "world_id": "world789",
    "data": {"prefab_id": "magic_tree_01"}
  }
]
```

### 4. Unity Integration

Prefab catalog for Unity client integration.

#### `GET /api/v1/prefab-catalog/`

Get the prefab catalog with optional filtering.

**Query Parameters:**
- `prefab_type` (string, optional): Filter by prefab type (`building`, `vehicle`, `character`, `prop`, `environment`, `lighting`, `effect`, `ui`)
- `limit` (integer, optional): Number of items per page (default: 50, max: 100)
- `offset` (integer, optional): Number of items to skip (default: 0)

**Response:**
```json
{
  "success": true,
  "prefabs": [
    {
      "id": "magic_tree_01",
      "name": "Enchanted Tree",
      "type": "environment",
      "description": "A mystical tree with glowing leaves and magical aura",
      "thumbnail_url": "https://example.com/thumbnails/magic_tree.jpg",
      "download_url": "https://example.com/prefabs/magic_tree_01.unitypackage",
      "size_bytes": 512000,
      "version": "1.0.0",
      "tags": ["fantasy", "nature", "magic", "environment"],
      "properties": {
        "poly_count": 2000,
        "animated": true,
        "glow_effect": true
      }
    }
  ],
  "total_count": 25,
  "page": 1,
  "page_size": 50
}
```

#### `GET /api/v1/prefab-catalog/{prefab_id}`

Get a specific prefab by ID.

**Response:**
```json
{
  "success": true,
  "prefabs": [
    {
      "id": "magic_tree_01",
      "name": "Enchanted Tree",
      "type": "environment",
      "description": "A mystical tree with glowing leaves and magical aura",
      "download_url": "https://example.com/prefabs/magic_tree_01.unitypackage",
      "size_bytes": 512000,
      "version": "1.0.0",
      "tags": ["fantasy", "nature", "magic"],
      "properties": {
        "poly_count": 2000,
        "animated": true,
        "glow_effect": true
      }
    }
  ],
  "total_count": 1,
  "page": 1,
  "page_size": 1
}
```

#### `GET /api/v1/prefab-catalog/search`

Search prefabs by name, description, or tags.

**Query Parameters:**
- `q` (string, required): Search query (1-100 characters)
- `prefab_type` (string, optional): Filter by prefab type
- `limit` (integer, optional): Number of results to return (default: 20, max: 50)

## Error Responses

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "ValidationError",
  "message": "Invalid input data",
  "details": {
    "field": "prompt",
    "issue": "Field is required"
  }
}
```

### Common HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Access denied
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## Rate Limiting

API requests are rate-limited to prevent abuse:
- **Authentication**: 10 requests per minute per IP
- **World Generation**: 5 requests per minute per user
- **Telemetry**: 100 requests per minute per user
- **General API**: 60 requests per minute per user

## Unity Integration Examples

### C# Unity Client Example

```csharp
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using System.Text;

public class ImmersiVerseClient : MonoBehaviour
{
    private string baseUrl = "http://localhost:8000/api/v1";
    private string authToken;
    
    // Create session
    public IEnumerator CreateSession(string userId)
    {
        var request = new UnityWebRequest($"{baseUrl}/auth/login", "POST");
        request.SetRequestHeader("Content-Type", "application/json");
        
        var body = $"{{\"user_id\": \"{userId}\"}}";
        request.uploadHandler = new UploadHandlerRaw(Encoding.UTF8.GetBytes(body));
        request.downloadHandler = new DownloadHandlerBuffer();
        
        yield return request.SendWebRequest();
        
        if (request.result == UnityWebRequest.Result.Success)
        {
            var response = JsonUtility.FromJson<AuthResponse>(request.downloadHandler.text);
            authToken = response.token;
        }
    }
    
    // Generate world from prompt
    public IEnumerator GenerateWorld(string prompt, string worldType)
    {
        var request = new UnityWebRequest($"{baseUrl}/prompt2world/", "POST");
        request.SetRequestHeader("Content-Type", "application/json");
        request.SetRequestHeader("Authorization", $"Bearer {authToken}");
        
        var body = $"{{\"prompt\": \"{prompt}\", \"world_type\": \"{worldType}\", \"user_id\": \"user123\"}}";
        request.uploadHandler = new UploadHandlerRaw(Encoding.UTF8.GetBytes(body));
        request.downloadHandler = new DownloadHandlerBuffer();
        
        yield return request.SendWebRequest();
        
        if (request.result == UnityWebRequest.Result.Success)
        {
            var response = JsonUtility.FromJson<PromptResponse>(request.downloadHandler.text);
            InstantiateWorld(response.world_blueprint);
        }
    }
    
    // Instantiate world in Unity
    private void InstantiateWorld(WorldBlueprint blueprint)
    {
        foreach (var prefabInstance in blueprint.prefab_instances)
        {
            // Download and instantiate prefab
            StartCoroutine(DownloadAndInstantiatePrefab(prefabInstance));
        }
        
        // Set spawn points
        foreach (var spawnPoint in blueprint.spawn_points)
        {
            // Configure player spawn points
        }
    }
    
    private IEnumerator DownloadAndInstantiatePrefab(PrefabInstance instance)
    {
        // Download prefab from catalog
        var catalogRequest = UnityWebRequest.Get($"{baseUrl}/prefab-catalog/{instance.prefab_id}");
        catalogRequest.SetRequestHeader("Authorization", $"Bearer {authToken}");
        yield return catalogRequest.SendWebRequest();
        
        if (catalogRequest.result == UnityWebRequest.Result.Success)
        {
            var catalogResponse = JsonUtility.FromJson<PrefabCatalogResponse>(catalogRequest.downloadHandler.text);
            var prefab = catalogResponse.prefabs[0];
            
            // Download prefab file
            var downloadRequest = UnityWebRequest.Get(prefab.download_url);
            yield return downloadRequest.SendWebRequest();
            
            if (downloadRequest.result == UnityWebRequest.Result.Success)
            {
                // Load and instantiate prefab
                // Implementation depends on your prefab loading system
            }
        }
    }
}

[System.Serializable]
public class AuthResponse
{
    public string user_id;
    public string session_id;
    public string token;
    public string expires_at;
    public string created_at;
}

[System.Serializable]
public class PromptResponse
{
    public bool success;
    public WorldBlueprint world_blueprint;
    public string message;
    public int processing_time_ms;
}

[System.Serializable]
public class WorldBlueprint
{
    public string id;
    public string prompt;
    public string world_type;
    public string title;
    public string description;
    public PrefabInstance[] prefab_instances;
    public Vector3[] spawn_points;
}

[System.Serializable]
public class PrefabInstance
{
    public string id;
    public string prefab_id;
    public string prefab_type;
    public Vector3 position;
    public Quaternion rotation;
    public Vector3 scale;
}
```

## Testing

Use the provided test suite to verify API functionality:

```bash
# Run all tests
pytest

# Run specific endpoint tests
pytest tests/test_prompt2world.py

# Run with coverage
pytest --cov=app --cov-report=html
```

## Support

For API support and questions:
- Check the interactive documentation at `/docs`
- Review the test cases in the `tests/` directory
- Create an issue in the repository
- Contact the development team

---

**API Version**: 1.0.0  
**Last Updated**: 2024-01-01  
**Maintained by**: ImmersiVerse OS Team
