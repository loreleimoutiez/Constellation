"""
Tests for base models (BaseAsset, TimestampMixin).
"""

import pytest
from datetime import datetime
from uuid import UUID

from app.models.base import (
    BaseAsset, 
    TimestampMixin, 
    CriticalityLevel, 
    EnvironmentType, 
    LifecycleState
)
from tests.factories import create_base_asset


class TestTimestampMixin:
    """Test TimestampMixin functionality."""
    
    def test_timestamp_mixin_creation(self):
        """Test that TimestampMixin creates timestamps correctly."""
        mixin = TimestampMixin()
        
        assert isinstance(mixin.created_at, datetime)
        assert isinstance(mixin.updated_at, datetime)
        assert mixin.since is None
        assert mixin.until is None
    
    def test_timestamp_mixin_with_custom_values(self):
        """Test TimestampMixin with custom timestamp values."""
        custom_time = datetime(2025, 1, 1, 12, 0, 0)
        
        mixin = TimestampMixin(
            since=custom_time,
            until=custom_time
        )
        
        assert mixin.since == custom_time
        assert mixin.until == custom_time


class TestCriticalityLevel:
    """Test CriticalityLevel enum."""
    
    def test_criticality_values(self):
        """Test all criticality level values."""
        assert CriticalityLevel.LOW == "LOW"
        assert CriticalityLevel.MEDIUM == "MEDIUM"
        assert CriticalityLevel.HIGH == "HIGH"
        assert CriticalityLevel.CRITICAL == "CRITICAL"
    
    def test_criticality_enum_membership(self):
        """Test criticality enum membership."""
        assert CriticalityLevel.LOW in CriticalityLevel
        assert "LOW" in [member.value for member in CriticalityLevel]
        assert "INVALID" not in [member.value for member in CriticalityLevel]


class TestEnvironmentType:
    """Test EnvironmentType enum."""
    
    def test_environment_values(self):
        """Test all environment type values."""
        assert EnvironmentType.DEVELOPMENT == "DEV"
        assert EnvironmentType.TESTING == "TEST"
        assert EnvironmentType.STAGING == "STAGING"
        assert EnvironmentType.PRODUCTION == "PROD"
        assert EnvironmentType.SANDBOX == "SANDBOX"


class TestLifecycleState:
    """Test LifecycleState enum."""
    
    def test_lifecycle_values(self):
        """Test all lifecycle state values."""
        assert LifecycleState.PLANNED == "PLANNED"
        assert LifecycleState.ACTIVE == "ACTIVE"
        assert LifecycleState.DEPRECATED == "DEPRECATED"
        assert LifecycleState.RETIRED == "RETIRED"
        assert LifecycleState.UNKNOWN == "UNKNOWN"


class TestBaseAsset:
    """Test BaseAsset model."""
    
    def test_base_asset_creation_minimal(self):
        """Test creating BaseAsset with minimal required fields."""
        asset = create_base_asset(name="Test Asset")
        
        # Check required fields
        assert asset.name == "Test Asset"
        
        # Check default values
        assert asset.criticality == CriticalityLevel.MEDIUM
        assert asset.environment == EnvironmentType.PRODUCTION
        assert asset.lifecycle_state == LifecycleState.ACTIVE
        assert asset.pii is False
        
        # Check generated ID is valid UUID
        assert isinstance(UUID(asset.id), UUID)
        
        # Check timestamps are set
        assert isinstance(asset.created_at, datetime)
        assert isinstance(asset.updated_at, datetime)
    
    def test_base_asset_creation_full(self):
        """Test creating BaseAsset with all fields."""
        asset_data = {
            "name": "Critical Production Server",
            "description": "Main application server",
            "criticality": CriticalityLevel.CRITICAL,
            "environment": EnvironmentType.PRODUCTION,
            "lifecycle_state": LifecycleState.ACTIVE,
            "owner": "john.doe",
            "confidentiality": "HIGH",
            "integrity": "HIGH", 
            "availability": "HIGH",
            "pii": True,
            "version": "1.2.3",
            "evidence_ref": "DOC-001"
        }
        
        asset = BaseAsset(**asset_data)
        
        # Verify all fields are set correctly
        for key, value in asset_data.items():
            assert getattr(asset, key) == value
    
    def test_base_asset_validation_errors(self):
        """Test BaseAsset validation errors."""
        # Test empty name
        with pytest.raises(ValueError):
            create_base_asset(name="")
        
        # Test name too long (over 255 chars)
        with pytest.raises(ValueError):
            create_base_asset(name="x" * 256)
        
        # Test description too long (over 1000 chars)  
        with pytest.raises(ValueError):
            create_base_asset(name="Test", description="x" * 1001)
    
    def test_base_asset_json_serialization(self):
        """Test BaseAsset JSON serialization."""
        asset = create_base_asset(
            name="Test Asset",
            criticality=CriticalityLevel.HIGH,
            environment=EnvironmentType.STAGING
        )
        
        # Test JSON export
        json_data = asset.model_dump()
        
        assert json_data["name"] == "Test Asset"
        assert json_data["criticality"] == "HIGH"
        assert json_data["environment"] == "STAGING"
        assert "id" in json_data
        assert "created_at" in json_data
    
    def test_base_asset_custom_id(self):
        """Test BaseAsset with custom ID."""
        custom_id = "custom-asset-123"
        asset = create_base_asset(id=custom_id, name="Test Asset")
        
        assert asset.id == custom_id
    
    def test_base_asset_defaults(self):
        """Test BaseAsset default values are applied correctly."""
        asset = create_base_asset(name="Test")
        
        # Test enum defaults
        assert asset.criticality == CriticalityLevel.MEDIUM
        assert asset.environment == EnvironmentType.PRODUCTION
        assert asset.lifecycle_state == LifecycleState.ACTIVE
        
        # Test that factory provided non-None values for required fields
        assert asset.description is not None
        assert asset.owner is not None
        assert asset.since is None
        assert asset.until is None
        
        # Test boolean defaults
        assert asset.pii is False