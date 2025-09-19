"""
Tests for CI (Configuration Item) models.
"""

import pytest
from uuid import UUID

from app.models.ci import CI, CIType
from app.models.base import CriticalityLevel, EnvironmentType
from tests.factories import create_ci


class TestCIType:
    """Test CIType enum."""
    
    def test_ci_type_values(self):
        """Test all CI type values."""
        assert CIType.HARDWARE == "HARDWARE"
        assert CIType.SOFTWARE == "SOFTWARE"
        assert CIType.NETWORK == "NETWORK"
        assert CIType.APPLICATION == "APPLICATION"
        assert CIType.SERVICE == "SERVICE"
        assert CIType.ENDPOINT == "ENDPOINT"
        assert CIType.DATASET == "DATASET"
        assert CIType.DATABASE == "DATABASE"
        assert CIType.LOCATION == "LOCATION"
        assert CIType.FACILITY == "FACILITY"
        assert CIType.IDENTITY == "IDENTITY"
        assert CIType.CREDENTIAL == "CREDENTIAL"
        assert CIType.GENERIC == "GENERIC"
    
    def test_ci_type_enum_membership(self):
        """Test CI type enum membership."""
        assert CIType.HARDWARE in CIType
        assert "HARDWARE" in [member.value for member in CIType]
        assert "INVALID_TYPE" not in [member.value for member in CIType]


class TestCI:
    """Test CI model."""
    
    def test_ci_creation_minimal(self, sample_ci_data):
        """Test creating CI with minimal required fields."""
        ci = create_ci(name="Test CI")
        
        # Check required fields
        assert ci.name == "Test CI"
        
        # Check CI-specific defaults
        assert ci.ci_type == CIType.GENERIC
        assert ci.monitoring_enabled is True
        assert ci.backup_enabled is False
        assert ci.custom_attributes == {}
        
        # Check inherited defaults from BaseAsset
        assert ci.criticality == CriticalityLevel.MEDIUM
        assert ci.environment == EnvironmentType.PRODUCTION
        
        # Check generated ID is valid UUID
        assert isinstance(UUID(ci.id), UUID)
    
    def test_ci_creation_full(self, sample_ci_data):
        """Test creating CI with all fields."""
        ci = create_ci(**sample_ci_data)
        
        # Verify all fields are set correctly
        assert ci.name == sample_ci_data["name"]
        assert ci.description == sample_ci_data["description"]
        assert ci.ci_type == CIType.HARDWARE
        assert ci.criticality == CriticalityLevel.HIGH
        assert ci.hostname == sample_ci_data["hostname"]
        assert ci.ip_address == sample_ci_data["ip_address"]
        assert ci.vendor == sample_ci_data["vendor"]
        assert ci.model == sample_ci_data["model"]
        assert ci.serial_number == sample_ci_data["serial_number"]
    
    def test_ci_with_network_details(self):
        """Test CI with network-specific details."""
        ci = create_ci(
            name="Web Server",
            ci_type=CIType.HARDWARE,
            hostname="web01.example.com",
            ip_address="10.0.1.100",
            fqdn="web01.prod.example.com"
        )
        
        assert ci.hostname == "web01.example.com"
        assert ci.ip_address == "10.0.1.100"
        assert ci.fqdn == "web01.prod.example.com"
    
    def test_ci_with_physical_details(self):
        """Test CI with physical location details."""
        ci = create_ci(
            name="Database Server",
            ci_type=CIType.HARDWARE,
            location="Datacenter A",
            rack_position="R42-U10",
            asset_tag="ASSET-001234"
        )
        
        assert ci.location == "Datacenter A"
        assert ci.rack_position == "R42-U10"
        assert ci.asset_tag == "ASSET-001234"
    
    def test_ci_with_operational_flags(self):
        """Test CI with operational configuration."""
        ci = create_ci(
            name="Monitoring Server",
            monitoring_enabled=False,
            backup_enabled=True,
            status="ACTIVE"
        )
        
        assert ci.monitoring_enabled is False
        assert ci.backup_enabled is True
        assert ci.status == "ACTIVE"
    
    def test_ci_with_compliance_tags(self):
        """Test CI with compliance and governance data."""
        ci = create_ci(
            name="PII Database",
            pii=True,
            compliance_tags=["GDPR", "HIPAA", "SOX"],
            cost_center="IT-001"
        )
        
        assert ci.pii is True
        assert ci.compliance_tags == ["GDPR", "HIPAA", "SOX"]
        assert ci.cost_center == "IT-001"
    
    def test_ci_with_custom_attributes(self):
        """Test CI with custom attributes."""
        custom_attrs = {
            "cpu_cores": 16,
            "memory_gb": 64,
            "storage_type": "SSD",
            "warranty_end": "2026-12-31"
        }
        
        ci = create_ci(
            name="High-Performance Server",
            custom_attributes=custom_attrs
        )
        
        assert ci.custom_attributes == custom_attrs
        assert ci.custom_attributes["cpu_cores"] == 16
        assert ci.custom_attributes["memory_gb"] == 64
    
    def test_ci_string_representations(self):
        """Test CI string and repr methods."""
        ci = create_ci(
            name="Test Server",
            ci_type=CIType.HARDWARE
        )
        
        # Test __str__ method
        str_repr = str(ci)
        assert "HARDWARE" in str_repr
        assert "Test Server" in str_repr
        assert ci.id in str_repr
        
        # Test __repr__ method
        repr_str = repr(ci)
        assert "CI(" in repr_str
        assert f"id='{ci.id}'" in repr_str
        assert "name='Test Server'" in repr_str
        assert "type='HARDWARE'" in repr_str
    
    def test_ci_json_serialization(self):
        """Test CI JSON serialization."""
        ci = create_ci(
            name="API Gateway",
            ci_type=CIType.SERVICE,
            criticality=CriticalityLevel.CRITICAL,
            hostname="api.example.com"
        )
        
        # Test JSON export
        json_data = ci.model_dump()
        
        assert json_data["name"] == "API Gateway"
        assert json_data["ci_type"] == "SERVICE"
        assert json_data["criticality"] == "CRITICAL"
        assert json_data["hostname"] == "api.example.com"
        assert "id" in json_data
        assert "created_at" in json_data
    
    def test_ci_inheritance_from_base_asset(self):
        """Test that CI properly inherits from BaseAsset."""
        ci = create_ci(name="Test CI")
        
        # Should have all BaseAsset attributes
        assert hasattr(ci, 'created_at')
        assert hasattr(ci, 'updated_at')
        assert hasattr(ci, 'criticality')
        assert hasattr(ci, 'environment')
        assert hasattr(ci, 'lifecycle_state')
        assert hasattr(ci, 'owner')
        assert hasattr(ci, 'pii')
        
        # Should have CI-specific attributes
        assert hasattr(ci, 'ci_type')
        assert hasattr(ci, 'hostname')
        assert hasattr(ci, 'custom_attributes')