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
def sample_human_data():
    """Sample human asset data for testing."""
    return {
        "name": "Jane Doe",
        "employee_id": "EMP001",
        "email": "jane.doe@company.com",
        "display_name": "Jane",
        "employment_status": "ACTIVE",
        "department": "Engineering",
        "is_manager": False,
        "on_call_enabled": True,
    }


@pytest.fixture
def sample_team_data():
    """Sample team data for testing."""
    return {
        "name": "DevOps Team",
        "team_type": "DEVOPS",
        "department": "Engineering",
        "primary_location": "San Francisco",
        "contact_email": "devops@company.com",
    }


@pytest.fixture
def sample_role_data():
    """Sample role data for testing."""
    return {
        "name": "Senior Software Engineer",
        "role_type": "TECHNICAL",
        "level": "Senior",
        "department": "Engineering",
        "is_on_call_role": True,
        "responsibilities": ["Development", "Code Review"],
        "required_skills": ["Python", "FastAPI"],
    }


@pytest.fixture
def freeze_time(monkeypatch):
    """Freeze time for consistent timestamp testing."""
    frozen_time = datetime(2025, 9, 17, 12, 0, 0)

    def mock_utcnow():
        return frozen_time

    monkeypatch.setattr(
        "app.models.base.datetime",
        type("MockDateTime", (), {"utcnow": staticmethod(mock_utcnow)}),
    )
    return frozen_time
