"""
Configuration Item (CI) models.

This module defines the core Configuration Item types and their
specialized variants for different asset categories.
"""

from enum import Enum
from typing import Optional, Dict, Any

from pydantic import Field

from .base import BaseAsset


class CIType(str, Enum):
    """Types of Configuration Items."""
    
    # Infrastructure
    HARDWARE = "HARDWARE"
    SOFTWARE = "SOFTWARE" 
    NETWORK = "NETWORK"
    
    # Applications and Services
    APPLICATION = "APPLICATION"
    SERVICE = "SERVICE"
    ENDPOINT = "ENDPOINT"
    
    # Data and Content
    DATASET = "DATASET"
    DATABASE = "DATABASE"
    
    # Physical and Location
    LOCATION = "LOCATION"
    FACILITY = "FACILITY"
    
    # Security and Identity
    IDENTITY = "IDENTITY"
    CREDENTIAL = "CREDENTIAL"
    
    # Generic fallback
    GENERIC = "GENERIC"


class CI(BaseAsset):
    """
    Core Configuration Item model.
    
    Represents any manageable component in the IT infrastructure,
    from physical hardware to virtual services and data assets.
    """
    
    # CI-specific attributes
    ci_type: CIType = CIType.GENERIC
    
    # Technical attributes
    hostname: Optional[str] = Field(None, description="Network hostname if applicable")
    ip_address: Optional[str] = Field(None, description="Primary IP address")
    fqdn: Optional[str] = Field(None, description="Fully qualified domain name")
    
    # Vendor and support information
    vendor: Optional[str] = Field(None, description="Vendor or manufacturer")
    model: Optional[str] = Field(None, description="Model or product name")
    serial_number: Optional[str] = Field(None, description="Serial number")
    asset_tag: Optional[str] = Field(None, description="Organization asset tag")
    
    # Location and deployment
    location: Optional[str] = Field(None, description="Physical or logical location")
    rack_position: Optional[str] = Field(None, description="Rack and position if applicable")
    
    # Operational attributes
    status: Optional[str] = Field(None, description="Operational status")
    monitoring_enabled: bool = Field(True, description="Whether monitoring is enabled")
    backup_enabled: bool = Field(False, description="Whether backup is enabled")
    
    # Compliance and governance
    compliance_tags: Optional[list[str]] = Field(default_factory=list, description="Compliance frameworks")
    cost_center: Optional[str] = Field(None, description="Cost center or budget code")
    
    # Flexible attributes for extensibility
    custom_attributes: Dict[str, Any] = Field(default_factory=dict, description="Custom key-value attributes")
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        
    def __str__(self) -> str:
        """String representation."""
        return f"{self.ci_type}: {self.name} ({self.id})"
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"CI(id='{self.id}', name='{self.name}', type='{self.ci_type}')"