"""
Configuration settings for the Constellation CMDB application.
"""
import os
from typing import Optional, List
from pydantic import BaseModel, field_validator


class Settings(BaseModel):
    """Application settings with environment variable support."""
    
    # API Configuration
    app_name: str = "Constellation"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Neo4j Database Configuration
    neo4j_uri: str = "bolt://neo4j:7687"
    neo4j_username: str = "neo4j"
    neo4j_password: str = "constellation123"
    
    # API Configuration
    api_prefix: str = "/api/v1"
    cors_origins: List[str] = [
        "http://localhost:3000", 
        "http://localhost:8080", 
        "http://localhost:5173"  # Vite dev server
    ]
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    @field_validator('neo4j_uri')
    @classmethod
    def validate_neo4j_uri(cls, v):
        if not v.startswith(('bolt://', 'neo4j://', 'bolt+s://', 'neo4j+s://')):
            raise ValueError('Neo4j URI must start with bolt:// or neo4j://')
        return v
    
    @field_validator('secret_key')
    @classmethod
    def validate_secret_key(cls, v):
        if v == "your-secret-key-change-in-production":
            print("WARNING: Using default secret key. Change this in production!")
        return v
    
    def __init__(self, **kwargs):
        # Load from environment variables
        env_values = {}
        for field_name in self.model_fields:
            env_name = field_name.upper()
            if env_name in os.environ:
                env_values[field_name] = os.environ[env_name]
        
        # Override with any provided kwargs
        env_values.update(kwargs)
        super().__init__(**env_values)


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings