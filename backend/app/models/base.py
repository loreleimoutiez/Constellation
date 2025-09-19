"""
Base models for all Constellation CMDB entities.

This module provides the foundational classes and mixins used by all
other model types in the system.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field, ConfigDict


class TimestampMixin(BaseModel):
    """Mixin for timestamp tracking."""
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    since: Optional[datetime] = None  # Valid from
    until: Optional[datetime] = None  # Valid until


class CriticalityLevel(str, Enum):
    """Asset criticality levels."""
    
    LOW = "LOW"
    MEDIUM = "MEDIUM" 
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class EnvironmentType(str, Enum):
    """Environment types."""
    
    DEVELOPMENT = "DEV"
    TESTING = "TEST"
    STAGING = "STAGING"
    PRODUCTION = "PROD"
    SANDBOX = "SANDBOX"


class LifecycleState(str, Enum):
    """Asset lifecycle states."""
    
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE" 
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"
    UNKNOWN = "UNKNOWN"


class BaseAsset(TimestampMixin):
    """Base class for all trackable assets in the CMDB."""
    
    # Core identification
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    
    # Asset metadata
    criticality: CriticalityLevel = CriticalityLevel.MEDIUM
    environment: EnvironmentType = EnvironmentType.PRODUCTION
    lifecycle_state: LifecycleState = LifecycleState.ACTIVE
    
    # Ownership and responsibility
    owner: Optional[str] = Field(None, description="ID of the owning person or team")
    
    # Data classification
    confidentiality: Optional[str] = Field(None, description="Data confidentiality level")
    integrity: Optional[str] = Field(None, description="Data integrity requirements")
    availability: Optional[str] = Field(None, description="Data availability requirements")
    pii: bool = Field(False, description="Contains personally identifiable information")
    
    # Audit and compliance
    version: Optional[str] = Field(None, description="Asset version")
    evidence_ref: Optional[str] = Field(None, description="Reference to supporting evidence")
    
    model_config = ConfigDict(use_enum_values=True)