"""
Tests for governance models (Policy, Risk, Process, Control, Vendor, Contract).
"""

import pytest
from datetime import datetime
from uuid import UUID
from pydantic import HttpUrl

from app.models.governance import (
    Policy,
    Risk,
    Process,
    Control,
    Vendor,
    Contract,
    PolicyType,
    PolicyStatus,
    RiskLevel,
    RiskStatus,
    ProcessType,
    ControlType,
    VendorType,
)


# Common fixture data for BaseAsset required fields
@pytest.fixture
def base_asset_data():
    """Common data for BaseAsset required fields."""
    return {
        "description": "Test description",
        "owner": "test-owner",
        "confidentiality": "INTERNAL",
        "integrity": "HIGH",
        "availability": "HIGH",
        "pii": False,
        "version": "1.0",
        "evidence_ref": "TEST-001",
    }


@pytest.fixture
def policy_required_data(base_asset_data):
    """Required data for Policy creation."""
    return {
        **base_asset_data,
        "policy_number": "POL-001",
        "approved_by": "CISO",
        "approved_at": datetime.now(),
        "effective_date": datetime.now(),
        "review_date": datetime(2025, 12, 31),
        "expiry_date": datetime(2026, 12, 31),
        "purpose": "Test policy purpose",
        "scope": "Test scope",
        "policy_text": "Policy content here",
        "mandatory": True,
        "enforcement_level": "HIGH",
        "exceptions_allowed": False,
        "document_url": None,
        "training_required": True,
    }


@pytest.fixture
def risk_required_data(base_asset_data):
    """Required data for Risk creation."""
    return {
        **base_asset_data,
        "likelihood": 3,
        "impact": 4,
        "risk_score": 12.0,
        "threat_source": "External threat",
        "vulnerability": "System vulnerability",
        "threat_event": "Security incident",
        "business_impact": "Service disruption",
        "financial_impact": 50000.0,
        "operational_impact": "High",
        "risk_owner": "security-team",
        "mitigation_strategy": "Implement controls",
        "target_resolution": datetime(2025, 12, 31),
        "last_assessment": datetime.now(),
        "next_review": datetime(2025, 6, 30),
        "residual_likelihood": 2,
        "residual_impact": 3,
        "residual_score": 6.0,
    }


@pytest.fixture
def process_required_data(base_asset_data):
    """Required data for Process creation."""
    return {
        **base_asset_data,
        "process_id": "PROC-001",
        "purpose": "Process purpose",
        "scope": "Process scope",
        "process_owner": "process-owner",
        "frequency": "Daily",
        "duration": "2 hours",
        "automation_level": "Manual",
        "procedure_url": None,
        "flowchart_url": None,
        "last_review": datetime.now(),
        "next_review": datetime(2025, 12, 31),
    }


@pytest.fixture
def control_required_data(base_asset_data):
    """Required data for Control creation."""
    return {
        **base_asset_data,
        "control_id": "CTRL-001",
        "objective": "Control objective",
        "description_text": "Control description",
        "implementation_guidance": "Implementation guide",
        "testing_procedures": "Testing procedures",
        "is_automated": False,
        "effectiveness_rating": "HIGH",
        "test_frequency": "Annual",
        "last_test_date": datetime.now(),
        "next_test_date": datetime(2025, 12, 31),
        "test_results": "PASS",
        "control_owner": "control-owner",
        "responsible_party": "responsible-party",
    }


@pytest.fixture
def vendor_required_data(base_asset_data):
    """Required data for Vendor creation."""
    return {
        **base_asset_data,
        "trading_name": "Trading Name",
        "registration_number": "REG123",
        "tax_id": "TAX456",
        "primary_contact": "John Doe",
        "email": "contact@vendor.com",
        "phone": "+1-555-0100",
        "website": "https://vendor.com",
        "address": "123 Main St",
        "city": "Test City",
        "country": "USA",
        "relationship_start": datetime(2025, 1, 1),
        "relationship_status": "ACTIVE",
        "risk_rating": "LOW",
        "annual_spend": 10000.0,
        "payment_terms": "Net 30",
        "sla_compliance": 95.0,
        "performance_rating": "GOOD",
    }


@pytest.fixture
def contract_required_data(base_asset_data):
    """Required data for Contract creation."""
    return {
        **base_asset_data,
        "contract_number": "CONT-001",
        "contract_type": "Service Agreement",
        "vendor_id": "vendor-001",
        "internal_owner": "procurement",
        "effective_date": datetime(2025, 1, 1),
        "expiry_date": datetime(2026, 1, 1),
        "notice_period": "30 days",
        "contract_value": 50000.0,
        "payment_schedule": "Monthly",
        "currency": "USD",
        "contract_url": None,
        "auto_renewal": False,
        "renewal_period": "1 year",
    }


class TestPolicyType:
    """Test PolicyType enum."""

    def test_policy_type_values(self):
        """Test all policy type values."""
        assert PolicyType.SECURITY == "SECURITY"
        assert PolicyType.PRIVACY == "PRIVACY"
        assert PolicyType.COMPLIANCE == "COMPLIANCE"
        assert PolicyType.OPERATIONAL == "OPERATIONAL"
        assert PolicyType.TECHNICAL == "TECHNICAL"
        assert PolicyType.BUSINESS == "BUSINESS"
        assert PolicyType.HR == "HR"
        assert PolicyType.FINANCIAL == "FINANCIAL"


class TestPolicyStatus:
    """Test PolicyStatus enum."""

    def test_policy_status_values(self):
        """Test all policy status values."""
        assert PolicyStatus.DRAFT == "DRAFT"
        assert PolicyStatus.REVIEW == "REVIEW"
        assert PolicyStatus.APPROVED == "APPROVED"
        assert PolicyStatus.ACTIVE == "ACTIVE"
        assert PolicyStatus.DEPRECATED == "DEPRECATED"
        assert PolicyStatus.RETIRED == "RETIRED"


class TestRiskLevel:
    """Test RiskLevel enum."""

    def test_risk_level_values(self):
        """Test all risk level values."""
        assert RiskLevel.VERY_LOW == "VERY_LOW"
        assert RiskLevel.LOW == "LOW"
        assert RiskLevel.MEDIUM == "MEDIUM"
        assert RiskLevel.HIGH == "HIGH"
        assert RiskLevel.VERY_HIGH == "VERY_HIGH"
        assert RiskLevel.CRITICAL == "CRITICAL"


class TestRiskStatus:
    """Test RiskStatus enum."""

    def test_risk_status_values(self):
        """Test all risk status values."""
        assert RiskStatus.IDENTIFIED == "IDENTIFIED"
        assert RiskStatus.ASSESSED == "ASSESSED"
        assert RiskStatus.MITIGATED == "MITIGATED"
        assert RiskStatus.ACCEPTED == "ACCEPTED"
        assert RiskStatus.TRANSFERRED == "TRANSFERRED"
        assert RiskStatus.AVOIDED == "AVOIDED"
        assert RiskStatus.CLOSED == "CLOSED"


class TestProcessType:
    """Test ProcessType enum."""

    def test_process_type_values(self):
        """Test all process type values."""
        assert ProcessType.OPERATIONAL == "OPERATIONAL"
        assert ProcessType.MANAGEMENT == "MANAGEMENT"
        assert ProcessType.SUPPORT == "SUPPORT"
        assert ProcessType.COMPLIANCE == "COMPLIANCE"
        assert ProcessType.INCIDENT == "INCIDENT"
        assert ProcessType.CHANGE == "CHANGE"
        assert ProcessType.RELEASE == "RELEASE"
        assert ProcessType.BACKUP == "BACKUP"
        assert ProcessType.SECURITY == "SECURITY"


class TestPolicy:
    """Test Policy model."""

    def test_policy_creation_minimal(self, policy_required_data):
        """Test creating Policy with minimal required fields."""
        policy_data = {**policy_required_data, "name": "Data Protection Policy"}
        policy = Policy(**policy_data)

        # Check required fields
        assert policy.name == "Data Protection Policy"

        # Check defaults
        assert policy.policy_type == PolicyType.OPERATIONAL
        assert policy.status == PolicyStatus.DRAFT
        assert policy.version == "1.0"
        assert policy.frameworks == []
        assert policy.regulations == []
        assert policy.mandatory is True
        assert policy.exceptions_allowed is False
        assert policy.training_required is True

        # Check inherited from BaseAsset
        assert isinstance(UUID(policy.id), UUID)

    def test_policy_creation_full(self, policy_required_data):
        """Test creating Policy with all fields."""
        policy_data = {
            **policy_required_data,
            "name": "GDPR Data Protection Policy",
            "policy_type": PolicyType.PRIVACY,
            "status": PolicyStatus.ACTIVE,
            "frameworks": ["GDPR", "ISO 27001"],
            "regulations": ["GDPR", "CCPA"],
        }

        policy = Policy(**policy_data)

        # Verify key fields are set correctly
        assert policy.name == "GDPR Data Protection Policy"
        assert policy.policy_type == PolicyType.PRIVACY
        assert policy.status == PolicyStatus.ACTIVE
        assert policy.frameworks == ["GDPR", "ISO 27001"]
        assert policy.regulations == ["GDPR", "CCPA"]

    def test_policy_string_representations(self, policy_required_data):
        """Test Policy string and repr methods."""
        policy_data = {
            **policy_required_data,
            "name": "Security Policy",
            "policy_type": PolicyType.SECURITY,
        }
        policy = Policy(**policy_data)

        # Test __str__ method
        str_repr = str(policy)
        assert str_repr == "Policy: Security Policy (SECURITY)"

        # Test __repr__ method
        repr_str = repr(policy)
        assert "Policy(" in repr_str
        assert "name='Security Policy'" in repr_str
        assert "type='SECURITY'" in repr_str


class TestRisk:
    """Test Risk model."""

    def test_risk_creation_minimal(self, risk_required_data):
        """Test creating Risk with minimal required fields."""
        risk_data = {**risk_required_data, "name": "Data Breach Risk"}
        risk = Risk(**risk_data)

        # Check required fields
        assert risk.name == "Data Breach Risk"

        # Check defaults
        assert risk.risk_level == RiskLevel.MEDIUM
        assert risk.status == RiskStatus.IDENTIFIED
        assert risk.mitigation_controls == []
        assert isinstance(risk.identified_date, datetime)

    def test_risk_creation_full(self, risk_required_data):
        """Test creating Risk with all fields."""
        risk_data = {
            **risk_required_data,
            "name": "SQL Injection Vulnerability",
            "risk_level": RiskLevel.HIGH,
            "status": RiskStatus.MITIGATED,
            "mitigation_controls": ["control-001", "control-002"],
        }

        risk = Risk(**risk_data)

        # Verify key fields are set correctly
        assert risk.name == "SQL Injection Vulnerability"
        assert risk.risk_level == RiskLevel.HIGH
        assert risk.status == RiskStatus.MITIGATED
        assert risk.likelihood == 3
        assert risk.impact == 4
        assert risk.mitigation_controls == ["control-001", "control-002"]

    def test_risk_score_validation(self, base_asset_data):
        """Test risk likelihood and impact validation (1-5)."""
        # Valid scores
        risk_data = {
            **base_asset_data,
            "name": "Test Risk",
            "likelihood": 3,
            "impact": 4,
            "risk_score": 12.0,
            "threat_source": "Test",
            "vulnerability": "Test",
            "threat_event": "Test",
            "business_impact": "Test",
            "financial_impact": 1000.0,
            "operational_impact": "Test",
            "risk_owner": "test",
            "mitigation_strategy": "Test",
            "target_resolution": datetime.now(),
            "last_assessment": datetime.now(),
            "next_review": datetime.now(),
            "residual_likelihood": 2,
            "residual_impact": 3,
            "residual_score": 6.0,
        }

        risk = Risk(**risk_data)
        assert risk.likelihood == 3
        assert risk.impact == 4

        # Invalid likelihood
        with pytest.raises(ValueError):
            invalid_data = {**risk_data, "likelihood": 0}
            Risk(**invalid_data)

        with pytest.raises(ValueError):
            invalid_data = {**risk_data, "likelihood": 6}
            Risk(**invalid_data)

        # Invalid impact
        with pytest.raises(ValueError):
            invalid_data = {**risk_data, "impact": 0}
            Risk(**invalid_data)

        with pytest.raises(ValueError):
            invalid_data = {**risk_data, "impact": 6}
            Risk(**invalid_data)

    def test_risk_string_representations(self, risk_required_data):
        """Test Risk string and repr methods."""
        risk_data = {
            **risk_required_data,
            "name": "Server Failure",
            "risk_level": RiskLevel.HIGH,
        }
        risk = Risk(**risk_data)

        # Test __str__ method
        str_repr = str(risk)
        assert str_repr == "Risk: Server Failure (HIGH)"

        # Test __repr__ method
        repr_str = repr(risk)
        assert "Risk(" in repr_str
        assert "name='Server Failure'" in repr_str
        assert "level='HIGH'" in repr_str


class TestProcess:
    """Test Process model."""

    def test_process_creation_minimal(self, process_required_data):
        """Test creating Process with minimal required fields."""
        process_data = {**process_required_data, "name": "Incident Response"}
        process = Process(**process_data)

        # Check required fields
        assert process.name == "Incident Response"

        # Check defaults
        assert process.process_type == ProcessType.OPERATIONAL
        assert process.version == "1.0"
        assert process.inputs == []
        assert process.outputs == []
        assert process.stakeholders == []
        assert process.kpis == []
        assert process.sla_targets == {}
        assert process.improvement_opportunities == []

    def test_process_creation_full(self, process_required_data):
        """Test creating Process with all fields."""
        process_data = {
            **process_required_data,
            "name": "Change Management Process",
            "process_type": ProcessType.CHANGE,
            "inputs": ["Change Request", "Impact Assessment"],
            "outputs": ["Approved Change", "Change Record"],
            "stakeholders": ["dev-team", "ops-team", "security-team"],
            "kpis": ["Change Success Rate", "Emergency Changes %"],
            "sla_targets": {"approval_time": "2 hours", "success_rate": "99%"},
        }

        process = Process(**process_data)

        # Verify key fields are set correctly
        assert process.name == "Change Management Process"
        assert process.process_type == ProcessType.CHANGE
        assert process.inputs == ["Change Request", "Impact Assessment"]
        assert process.outputs == ["Approved Change", "Change Record"]
        assert process.stakeholders == ["dev-team", "ops-team", "security-team"]
        assert process.kpis == ["Change Success Rate", "Emergency Changes %"]
        assert process.sla_targets["success_rate"] == "99%"

    def test_process_string_representations(self, process_required_data):
        """Test Process string and repr methods."""
        process_data = {
            **process_required_data,
            "name": "Backup Process",
            "process_type": ProcessType.BACKUP,
        }
        process = Process(**process_data)

        # Test __str__ method
        str_repr = str(process)
        assert str_repr == "Process: Backup Process (BACKUP)"

        # Test __repr__ method
        repr_str = repr(process)
        assert "Process(" in repr_str
        assert "name='Backup Process'" in repr_str
        assert "type='BACKUP'" in repr_str


class TestControl:
    """Test Control model."""

    def test_control_creation_minimal(self, control_required_data):
        """Test creating Control with minimal required fields."""
        control_data = {**control_required_data, "name": "Access Control"}
        control = Control(**control_data)

        # Check required fields
        assert control.name == "Access Control"

        # Check defaults
        assert control.control_type == ControlType.PREVENTIVE
        assert control.is_automated is False
        assert control.frameworks == []
        assert control.control_families == []

    def test_control_creation_full(self, control_required_data):
        """Test creating Control with all fields."""
        control_data = {
            **control_required_data,
            "name": "Multi-Factor Authentication",
            "control_type": ControlType.PREVENTIVE,
            "is_automated": True,
            "frameworks": ["NIST", "ISO 27001"],
            "control_families": ["Access Control", "Authentication"],
        }

        control = Control(**control_data)

        # Verify key fields are set correctly
        assert control.name == "Multi-Factor Authentication"
        assert control.control_type == ControlType.PREVENTIVE
        assert control.is_automated is True
        assert control.frameworks == ["NIST", "ISO 27001"]
        assert control.control_families == ["Access Control", "Authentication"]

    def test_control_string_representation(self, control_required_data):
        """Test Control string representation."""
        control_data = {
            **control_required_data,
            "name": "Firewall Rules",
            "control_type": ControlType.PREVENTIVE,
        }
        control = Control(**control_data)

        str_repr = str(control)
        assert str_repr == "Control: Firewall Rules (PREVENTIVE)"


class TestVendor:
    """Test Vendor model."""

    def test_vendor_creation_minimal(self, vendor_required_data):
        """Test creating Vendor with minimal required fields."""
        vendor_data = {
            **vendor_required_data,
            "name": "AWS Services",
            "legal_name": "Amazon Web Services, Inc.",
        }
        vendor = Vendor(**vendor_data)

        # Check required fields
        assert vendor.name == "AWS Services"
        assert vendor.legal_name == "Amazon Web Services, Inc."

        # Check defaults
        assert vendor.vendor_type == VendorType.SERVICE
        assert vendor.services_provided == []
        assert vendor.capabilities == []
        assert vendor.compliance_certifications == []
        assert vendor.security_assessments == []

    def test_vendor_creation_full(self, vendor_required_data):
        """Test creating Vendor with all fields."""
        vendor_data = {
            **vendor_required_data,
            "name": "SecureCloud Corp",
            "legal_name": "SecureCloud Corporation",
            "vendor_type": VendorType.CLOUD,
            "services_provided": ["Cloud Hosting", "Security Monitoring"],
            "capabilities": ["24/7 Support", "SOC 2 Compliance"],
            "compliance_certifications": ["SOC 2", "ISO 27001"],
            "security_assessments": ["Penetration Test 2025"],
        }

        vendor = Vendor(**vendor_data)

        # Verify key fields are set correctly
        assert vendor.name == "SecureCloud Corp"
        assert vendor.legal_name == "SecureCloud Corporation"
        assert vendor.vendor_type == VendorType.CLOUD
        assert vendor.services_provided == ["Cloud Hosting", "Security Monitoring"]
        assert vendor.compliance_certifications == ["SOC 2", "ISO 27001"]

    def test_vendor_annual_spend_validation(self, base_asset_data):
        """Test vendor annual_spend validation (must be >= 0)."""
        vendor_base = {
            **base_asset_data,
            "name": "Test Vendor",
            "legal_name": "Test Vendor LLC",
            "trading_name": "Test",
            "registration_number": "REG123",
            "tax_id": "TAX456",
            "primary_contact": "John",
            "email": "test@test.com",
            "phone": "+1-555-0100",
            "website": "https://test.com",
            "address": "123 Main",
            "city": "City",
            "country": "USA",
            "relationship_start": datetime.now(),
            "relationship_status": "ACTIVE",
            "risk_rating": "LOW",
            "payment_terms": "Net 30",
            "sla_compliance": 95.0,
            "performance_rating": "GOOD",
        }

        # Valid spend
        vendor_data = {**vendor_base, "annual_spend": 10000.0}
        vendor = Vendor(**vendor_data)
        assert vendor.annual_spend == 10000.0

        # Invalid spend
        with pytest.raises(ValueError):
            invalid_data = {**vendor_base, "annual_spend": -1000.0}
            Vendor(**invalid_data)

    def test_vendor_sla_compliance_validation(self, base_asset_data):
        """Test vendor SLA compliance validation (0-100)."""
        vendor_base = {
            **base_asset_data,
            "name": "Test Vendor",
            "legal_name": "Test Vendor LLC",
            "trading_name": "Test",
            "registration_number": "REG123",
            "tax_id": "TAX456",
            "primary_contact": "John",
            "email": "test@test.com",
            "phone": "+1-555-0100",
            "website": "https://test.com",
            "address": "123 Main",
            "city": "City",
            "country": "USA",
            "relationship_start": datetime.now(),
            "relationship_status": "ACTIVE",
            "risk_rating": "LOW",
            "annual_spend": 10000.0,
            "payment_terms": "Net 30",
            "performance_rating": "GOOD",
        }

        # Valid compliance
        vendor_data = {**vendor_base, "sla_compliance": 95.5}
        vendor = Vendor(**vendor_data)
        assert vendor.sla_compliance == 95.5

        # Invalid compliance (over 100)
        with pytest.raises(ValueError):
            invalid_data = {**vendor_base, "sla_compliance": 101.0}
            Vendor(**invalid_data)

    def test_vendor_string_representations(self, vendor_required_data):
        """Test Vendor string and repr methods."""
        vendor_data = {
            **vendor_required_data,
            "name": "Cloud Provider",
            "legal_name": "Cloud Provider Inc.",
            "vendor_type": VendorType.CLOUD,
        }
        vendor = Vendor(**vendor_data)

        # Test __str__ method
        str_repr = str(vendor)
        assert str_repr == "Vendor: Cloud Provider Inc. (CLOUD)"

        # Test __repr__ method
        repr_str = repr(vendor)
        assert "Vendor(" in repr_str
        assert "name='Cloud Provider Inc.'" in repr_str
        assert "type='CLOUD'" in repr_str


class TestContract:
    """Test Contract model."""

    def test_contract_creation_minimal(self, contract_required_data):
        """Test creating Contract with minimal required fields."""
        contract_data = {**contract_required_data, "name": "Cloud Services Agreement"}
        contract = Contract(**contract_data)

        # Check required fields
        assert contract.name == "Cloud Services Agreement"

        # Check defaults
        assert contract.sla_terms == {}
        assert contract.penalties == {}
        assert contract.auto_renewal is False

    def test_contract_creation_full(self, contract_required_data):
        """Test creating Contract with all fields."""
        contract_data = {
            **contract_required_data,
            "name": "AWS Enterprise Agreement",
            "sla_terms": {"uptime": "99.9%", "response_time": "1 hour"},
            "penalties": {"downtime": "1% per hour", "breach": "10000 USD"},
            "auto_renewal": True,
        }

        contract = Contract(**contract_data)

        # Verify key fields are set correctly
        assert contract.name == "AWS Enterprise Agreement"
        assert contract.sla_terms["uptime"] == "99.9%"
        assert contract.penalties["downtime"] == "1% per hour"
        assert contract.auto_renewal is True

    def test_contract_value_validation(self, base_asset_data):
        """Test contract value validation (must be >= 0)."""
        contract_base = {
            **base_asset_data,
            "contract_number": "CONT-001",
            "contract_type": "Service",
            "vendor_id": "vendor-001",
            "internal_owner": "procurement",
            "effective_date": datetime.now(),
            "expiry_date": datetime(2026, 1, 1),
            "notice_period": "30 days",
            "payment_schedule": "Monthly",
            "currency": "USD",
            "contract_url": None,
            "auto_renewal": False,
            "renewal_period": "1 year",
        }

        # Valid value
        contract_data = {
            **contract_base,
            "name": "Test Contract",
            "contract_value": 25000.0,
        }
        contract = Contract(**contract_data)
        assert contract.contract_value == 25000.0

        # Invalid value
        with pytest.raises(ValueError):
            invalid_data = {
                **contract_base,
                "name": "Test Contract",
                "contract_value": -5000.0,
            }
            Contract(**invalid_data)

    def test_contract_string_representation(self, contract_required_data):
        """Test Contract string representation."""
        contract_data = {
            **contract_required_data,
            "name": "Support Agreement",
            "contract_number": "SUP-001",
        }
        contract = Contract(**contract_data)

        str_repr = str(contract)
        assert str_repr == "Contract: Support Agreement (SUP-001)"
