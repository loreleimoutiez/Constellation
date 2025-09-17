"""
Test configuration for Constellation backend.
"""

import pytest
from datetime import datetime
from uuid import uuid4


@pytest.fixture
def sample_ci_data():
    """Sample CI data for testing."""
    return {
        "name": "Test Server",
        "description": "A test server for unit testing",
        "ci_type": "HARDWARE",
        "criticality": "HIGH",
        "environment": "PROD",
        "hostname": "test-srv-01",
        "ip_address": "192.168.1.100",
        "vendor": "Dell",
        "model": "PowerEdge R740",
        "serial_number": "SN123456789",
    }


@pytest.fixture
def sample_relationship_data():
    """Sample relationship data for testing."""
    return {
        "source_id": str(uuid4()),
        "target_id": str(uuid4()),
        "relationship_type": "DEPENDS_ON",
        "strength": "STRONG",
        "description": "Test dependency relationship",
        "active": True,
    }


@pytest.fixture
def freeze_time(monkeypatch):
    """Freeze time for consistent timestamp testing."""
    frozen_time = datetime(2025, 9, 17, 12, 0, 0)
    
    def mock_utcnow():
        return frozen_time
    
    monkeypatch.setattr("app.models.base.datetime", type("MockDateTime", (), {"utcnow": staticmethod(mock_utcnow)}))
    return frozen_time