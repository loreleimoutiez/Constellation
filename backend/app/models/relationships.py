"""
Relationship models for the CMDB graph.

This module defines the types of relationships that can exist between
different assets and entities in the system.
"""

from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime

from pydantic import BaseModel, Field

from .base import TimestampMixin


class RelationshipType(str, Enum):
    """Types of relationships between assets."""
    
    # Technical dependencies
    DEPENDS_ON = "DEPENDS_ON"
    RUNS_ON = "RUNS_ON"
    HOSTS = "HOSTS"
    CONNECTS_TO = "CONNECTS_TO"
    INSTALLED_ON = "INSTALLED_ON"
    USES = "USES"
    
    # Data relationships
    PRODUCES = "PRODUCES"
    CONSUMES = "CONSUMES"
    PROCESSES = "PROCESSES"
    STORES = "STORES"
    
    # Human relationships
    OWNS = "OWNS"
    RESPONSIBLE_FOR = "RESPONSIBLE_FOR"
    ACCOUNTABLE_FOR = "ACCOUNTABLE_FOR"
    CONSULTED_FOR = "CONSULTED_FOR"
    INFORMED_FOR = "INFORMED_FOR"
    MEMBER_OF = "MEMBER_OF"
    HAS_ROLE = "HAS_ROLE"
    HAS_SKILL = "HAS_SKILL"
    
    # Governance relationships
    GOVERNED_BY = "GOVERNED_BY"
    SUBJECT_TO = "SUBJECT_TO"
    COMPLIES_WITH = "COMPLIES_WITH"
    PROTECTS = "PROTECTS"
    COVERS = "COVERS"
    
    # Business relationships
    OUTSOURCED_TO = "OUTSOURCED_TO"
    PROVIDED_BY = "PROVIDED_BY"
    COVERED_BY = "COVERED_BY"
    CONTRACTED_WITH = "CONTRACTED_WITH"
    
    # Knowledge relationships
    DOCUMENTS = "DOCUMENTS"
    KNOWS = "KNOWS"
    REFERENCES = "REFERENCES"
    
    # Generic
    RELATED_TO = "RELATED_TO"


class RelationshipStrength(str, Enum):
    """Strength of relationships for impact analysis."""
    
    WEAK = "WEAK"
    MEDIUM = "MEDIUM"
    STRONG = "STRONG"
    CRITICAL = "CRITICAL"


class Relationship(TimestampMixin):
    """
    Relationship between two assets.
    
    Represents a directed relationship from a source asset to a target asset,
    with metadata about the nature and strength of the relationship.
    """
    
    # Core relationship definition
    source_id: str = Field(..., description="ID of the source asset")
    target_id: str = Field(..., description="ID of the target asset")
    relationship_type: RelationshipType = Field(..., description="Type of relationship")
    
    # Relationship metadata
    strength: RelationshipStrength = RelationshipStrength.MEDIUM
    weight: float = Field(1.0, ge=0.0, le=10.0, description="Numeric weight for algorithms")
    
    # Descriptive information
    description: Optional[str] = Field(None, max_length=500, description="Human readable description")
    
    # Operational metadata
    active: bool = Field(True, description="Whether the relationship is currently active")
    verified: bool = Field(False, description="Whether the relationship has been verified")
    auto_discovered: bool = Field(False, description="Whether discovered automatically")
    
    # Context and conditions
    conditions: Optional[str] = Field(None, description="Conditions when this relationship applies")
    port: Optional[str] = Field(None, description="Network port if applicable")
    protocol: Optional[str] = Field(None, description="Protocol if applicable")
    
    # Audit trail
    discovered_by: Optional[str] = Field(None, description="Who or what discovered this relationship")
    discovered_at: Optional[datetime] = Field(None, description="When this relationship was discovered")
    last_verified: Optional[datetime] = Field(None, description="Last verification timestamp")
    
    # Flexible attributes
    custom_attributes: Dict[str, Any] = Field(default_factory=dict, description="Custom key-value attributes")
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.source_id} -{self.relationship_type}-> {self.target_id}"
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"Relationship(source='{self.source_id}', target='{self.target_id}', type='{self.relationship_type}')"
    
    @property
    def is_bidirectional(self) -> bool:
        """Check if this relationship type is typically bidirectional."""
        bidirectional_types = {
            RelationshipType.CONNECTS_TO,
            RelationshipType.RELATED_TO,
            RelationshipType.MEMBER_OF,
        }
        return self.relationship_type in bidirectional_types