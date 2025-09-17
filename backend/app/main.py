"""
Constellation CMDB - FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI application
app = FastAPI(
    title="Constellation CMDB API",
    description="Configuration Management Database API for IT Asset Management",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "Constellation CMDB API",
        "version": "0.1.0",
        "status": "running",
        "message": "Welcome to Constellation Configuration Management Database API"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "constellation-api",
        "version": "0.1.0"
    }


@app.get("/api/v1/status")
async def api_status():
    """API v1 status endpoint."""
    return {
        "api_version": "v1",
        "status": "operational",
        "features": {
            "authentication": "planned",
            "crud_operations": "planned",
            "impact_analysis": "planned",
            "graph_queries": "planned"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )