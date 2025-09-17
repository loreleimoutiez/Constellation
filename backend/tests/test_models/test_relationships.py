"""
Tests for Relationship models.
"""

import pytest
from datetime import datetime
from uuid import uuid4

from app.models.relationships import (
    Relationship, 
    RelationshipType, 
    RelationshipStrength
)


class TestRelationshipType:
    """Test RelationshipType enum."""
    
    def test_technical_relationship_types(self):
        """Test technical dependency relationship types."""
        assert RelationshipType.DEPENDS_ON == "DEPENDS_ON"
        assert RelationshipType.RUNS_ON == "RUNS_ON"
        assert RelationshipType.HOSTS == "HOSTS"
        assert RelationshipType.CONNECTS_TO == "CONNECTS_TO"
        assert RelationshipType.INSTALLED_ON == "INSTALLED_ON"
        assert RelationshipType.USES == "USES"
    
    def test_data_relationship_types(self):
        """Test data flow relationship types."""
        assert RelationshipType.PRODUCES == "PRODUCES"
        assert RelationshipType.CONSUMES == "CONSUMES"
        assert RelationshipType.PROCESSES == "PROCESSES"
        assert RelationshipType.STORES == "STORES"
    
    def test_human_relationship_types(self):
        """Test human/organizational relationship types."""
        assert RelationshipType.OWNS == "OWNS"
        assert RelationshipType.RESPONSIBLE_FOR == "RESPONSIBLE_FOR"
        assert RelationshipType.ACCOUNTABLE_FOR == "ACCOUNTABLE_FOR"
        assert RelationshipType.MEMBER_OF == "MEMBER_OF"
        assert RelationshipType.HAS_ROLE == "HAS_ROLE"
    
    def test_governance_relationship_types(self):
        """Test governance relationship types."""
        assert RelationshipType.GOVERNED_BY == "GOVERNED_BY"
        assert RelationshipType.SUBJECT_TO == "SUBJECT_TO"
        assert RelationshipType.COMPLIES_WITH == "COMPLIES_WITH"
        assert RelationshipType.PROTECTS == "PROTECTS"


class TestRelationshipStrength:
    """Test RelationshipStrength enum."""
    
    def test_strength_values(self):
        """Test all relationship strength values."""
        assert RelationshipStrength.WEAK == "WEAK"
        assert RelationshipStrength.MEDIUM == "MEDIUM"
        assert RelationshipStrength.STRONG == "STRONG"
        assert RelationshipStrength.CRITICAL == "CRITICAL"


class TestRelationship:
    """Test Relationship model."""
    
    def test_relationship_creation_minimal(self, sample_relationship_data):
        """Test creating Relationship with minimal required fields."""
        minimal_data = {
            "source_id": sample_relationship_data["source_id"],
            "target_id": sample_relationship_data["target_id"],
            "relationship_type": RelationshipType.DEPENDS_ON
        }
        
        rel = Relationship(**minimal_data)
        
        # Check required fields
        assert rel.source_id == minimal_data["source_id"]
        assert rel.target_id == minimal_data["target_id"]
        assert rel.relationship_type == RelationshipType.DEPENDS_ON
        
        # Check defaults
        assert rel.strength == RelationshipStrength.MEDIUM
        assert rel.weight == 1.0
        assert rel.active is True
        assert rel.verified is False
        assert rel.auto_discovered is False
        assert rel.custom_attributes == {}
    
    def test_relationship_creation_full(self, sample_relationship_data):
        """Test creating Relationship with all fields."""
        full_data = {
            **sample_relationship_data,
            "weight": 5.5,
            "verified": True,
            "auto_discovered": True,
            "conditions": "During business hours",
            "port": "443",
            "protocol": "HTTPS",
            "discovered_by": "network_scanner",
            "custom_attributes": {"latency_ms": 15, "bandwidth_mbps": 1000}
        }
        
        rel = Relationship(**full_data)
        
        # Verify all fields are set correctly
        assert rel.source_id == full_data["source_id"]
        assert rel.target_id == full_data["target_id"]
        assert rel.relationship_type == RelationshipType.DEPENDS_ON
        assert rel.strength == RelationshipStrength.STRONG
        assert rel.weight == 5.5
        assert rel.description == full_data["description"]
        assert rel.active is True
        assert rel.verified is True
        assert rel.auto_discovered is True
        assert rel.conditions == "During business hours"
        assert rel.port == "443"
        assert rel.protocol == "HTTPS"
        assert rel.discovered_by == "network_scanner"
        assert rel.custom_attributes["latency_ms"] == 15
    
    def test_relationship_weight_validation(self, sample_relationship_data):
        """Test relationship weight validation (0.0 to 10.0)."""
        # Test valid weights
        valid_weights = [0.0, 5.5, 10.0]
        for weight in valid_weights:
            rel = Relationship(**sample_relationship_data, weight=weight)
            assert rel.weight == weight
        
        # Test invalid weights
        with pytest.raises(ValueError):
            Relationship(**sample_relationship_data, weight=-1.0)
        
        with pytest.raises(ValueError):
            Relationship(**sample_relationship_data, weight=11.0)
    
    def test_relationship_timestamps(self, sample_relationship_data):
        """Test relationship timestamp handling."""
        discovery_time = datetime(2025, 9, 17, 10, 0, 0)
        verification_time = datetime(2025, 9, 17, 11, 0, 0)
        
        rel = Relationship(
            **sample_relationship_data,
            discovered_at=discovery_time,
            last_verified=verification_time
        )
        
        assert rel.discovered_at == discovery_time
        assert rel.last_verified == verification_time
        
        # Check inherited timestamps
        assert rel.created_at is not None
        assert rel.updated_at is not None
    
    def test_relationship_string_representations(self, sample_relationship_data):
        """Test Relationship string and repr methods."""
        rel = Relationship(**sample_relationship_data)
        
        # Test __str__ method
        str_repr = str(rel)
        expected_str = f"{rel.source_id} -DEPENDS_ON-> {rel.target_id}"
        assert str_repr == expected_str
        
        # Test __repr__ method
        repr_str = repr(rel)
        assert "Relationship(" in repr_str
        assert f"source='{rel.source_id}'" in repr_str
        assert f"target='{rel.target_id}'" in repr_str
        assert "type='DEPENDS_ON'" in repr_str
    
    def test_relationship_is_bidirectional_property(self):
        """Test is_bidirectional property for different relationship types."""
        source_id = str(uuid4())
        target_id = str(uuid4())
        
        # Test bidirectional relationships
        bidirectional_types = [
            RelationshipType.CONNECTS_TO,
            RelationshipType.RELATED_TO,
            RelationshipType.MEMBER_OF
        ]
        
        for rel_type in bidirectional_types:
            rel = Relationship(
                source_id=source_id,
                target_id=target_id,
                relationship_type=rel_type
            )
            assert rel.is_bidirectional is True
        
        # Test unidirectional relationships
        unidirectional_types = [
            RelationshipType.DEPENDS_ON,
            RelationshipType.RUNS_ON,
            RelationshipType.OWNS,
            RelationshipType.PRODUCES
        ]
        
        for rel_type in unidirectional_types:
            rel = Relationship(
                source_id=source_id,
                target_id=target_id,
                relationship_type=rel_type
            )
            assert rel.is_bidirectional is False
    
    def test_relationship_json_serialization(self, sample_relationship_data):
        """Test Relationship JSON serialization."""
        rel = Relationship(**sample_relationship_data)
        
        # Test JSON export
        json_data = rel.dict()
        
        assert json_data["source_id"] == sample_relationship_data["source_id"]
        assert json_data["target_id"] == sample_relationship_data["target_id"]
        assert json_data["relationship_type"] == "DEPENDS_ON"
        assert json_data["strength"] == "STRONG"
        assert json_data["active"] is True
        assert "created_at" in json_data
        assert "updated_at" in json_data
    
    def test_relationship_network_specific_fields(self):
        """Test relationship with network-specific fields."""
        source_id = str(uuid4())
        target_id = str(uuid4())
        
        rel = Relationship(
            source_id=source_id,
            target_id=target_id,
            relationship_type=RelationshipType.CONNECTS_TO,
            port="8080",
            protocol="HTTP",
            custom_attributes={
                "load_balancer": True,
                "ssl_enabled": False,
                "timeout_seconds": 30
            }
        )
        
        assert rel.port == "8080"
        assert rel.protocol == "HTTP"
        assert rel.custom_attributes["load_balancer"] is True
        assert rel.custom_attributes["ssl_enabled"] is False
    
    def test_relationship_audit_fields(self):
        """Test relationship audit and discovery fields."""
        source_id = str(uuid4())
        target_id = str(uuid4())
        
        rel = Relationship(
            source_id=source_id,
            target_id=target_id,
            relationship_type=RelationshipType.USES,
            auto_discovered=True,
            discovered_by="dependency_scanner",
            verified=True
        )
        
        assert rel.auto_discovered is True
        assert rel.discovered_by == "dependency_scanner"
        assert rel.verified is True