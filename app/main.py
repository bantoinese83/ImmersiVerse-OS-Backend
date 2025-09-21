"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.middleware import LoggingMiddleware, ErrorHandlingMiddleware
from app.api import auth, prompt2world, publish, telemetry, prefab_catalog
from app.schemas import ErrorResponse

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI backend for ImmersiVerse OS - transforms text prompts into immersive worlds",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

# Include API routers
app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(prompt2world.router, prefix=settings.api_v1_prefix)
app.include_router(publish.router, prefix=settings.api_v1_prefix)
app.include_router(telemetry.router, prefix=settings.api_v1_prefix)
app.include_router(prefab_catalog.router, prefix=settings.api_v1_prefix)


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to ImmersiVerse OS Backend",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "api_prefix": settings.api_v1_prefix
    }


@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "timestamp": "2024-01-01T00:00:00Z"  # This would be dynamic in production
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            error="InternalServerError",
            message="An unexpected error occurred",
            details={"path": str(request.url.path)}
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
