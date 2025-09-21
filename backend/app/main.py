"""
Constellation CMDB - FastAPI Backend Application
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import neo4j_connection
from .api import ci_endpoints, impact_endpoints

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown."""
    # Startup
    try:
        neo4j_connection.configure(
            uri=settings.neo4j_uri,
            username=settings.neo4j_username,
            password=settings.neo4j_password,
        )
        await neo4j_connection.connect()
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

    yield

    # Shutdown
    await neo4j_connection.disconnect()
    logger.info("Application shutdown complete")


# FastAPI application instance
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Open-source Configuration Management Database built with Neo4j",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
# Include routers
app.include_router(ci_endpoints.router, prefix=settings.api_prefix)
app.include_router(impact_endpoints.router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    """Root endpoint with basic application information."""
    return {
        "message": "Welcome to Constellation",
        "version": settings.app_version,
        "status": "operational",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Check Neo4j connectivity
        await neo4j_connection.verify_connectivity()
        return {
            "status": "healthy",
            "database": "connected",
            "version": settings.app_version,
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@app.get("/api/v1/status")
async def api_status():
    """API status endpoint with detailed information."""
    return {
        "api_version": "v1",
        "status": "operational",
        "database_connected": neo4j_connection.is_connected,
        "endpoints": {
            "health": "/health",
            "root": "/",
            "docs": "/docs",
            "openapi": "/openapi.json",
        },
    }


@app.get("/api/v1/database/test")
async def test_database():
    """Test database connectivity and basic operations."""
    try:
        # Test basic query
        result = await neo4j_connection.execute_query(
            "RETURN 'Neo4j connected!' as message, datetime() as timestamp"
        )

        # Test database version
        version_result = await neo4j_connection.execute_query(
            "CALL dbms.components() YIELD name, versions RETURN name, versions[0] as version"
        )

        return {
            "status": "success",
            "message": result[0]["message"] if result else "Unknown",
            "timestamp": str(result[0]["timestamp"]) if result else "Unknown",
            "database_info": version_result[0] if version_result else "Unknown",
        }
    except Exception as e:
        logger.error(f"Database test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database test failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
