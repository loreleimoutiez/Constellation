"""
Governance models for policies, risks, processes, and compliance.

This module defines models for tracking governance elements,
compliance frameworks, risk management, and business processes.
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime

from pydantic import Field, HttpUrl, ConfigDict

from .base import BaseAsset, TimestampMixin


class PolicyType(str, Enum):
    """Types of policies."""
    
    SECURITY = "SECURITY"
    PRIVACY = "PRIVACY"
    COMPLIANCE = "COMPLIANCE"
    OPERATIONAL = "OPERATIONAL"
    TECHNICAL = "TECHNICAL"
    BUSINESS = "BUSINESS"
    HR = "HR"
    FINANCIAL = "FINANCIAL"


class PolicyStatus(str, Enum):
    """Policy lifecycle status."""
    
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"


class RiskLevel(str, Enum):
    """Risk level classification."""
    
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"
    CRITICAL = "CRITICAL"


class RiskStatus(str, Enum):
    """Risk management status."""
    
    IDENTIFIED = "IDENTIFIED"
    ASSESSED = "ASSESSED"
    MITIGATED = "MITIGATED"
    ACCEPTED = "ACCEPTED"
    TRANSFERRED = "TRANSFERRED"
    AVOIDED = "AVOIDED"
    CLOSED = "CLOSED"


class ProcessType(str, Enum):
    """Types of business processes."""
    
    OPERATIONAL = "OPERATIONAL"
    MANAGEMENT = "MANAGEMENT"
    SUPPORT = "SUPPORT"
    COMPLIANCE = "COMPLIANCE"
    INCIDENT = "INCIDENT"
    CHANGE = "CHANGE"
    RELEASE = "RELEASE"
    BACKUP = "BACKUP"
    SECURITY = "SECURITY"


class ControlType(str, Enum):
    """Types of controls."""
    
    PREVENTIVE = "PREVENTIVE"
    DETECTIVE = "DETECTIVE"
    CORRECTIVE = "CORRECTIVE"
    COMPENSATING = "COMPENSATING"
    DIRECTIVE = "DIRECTIVE"


class VendorType(str, Enum):
    """Types of vendors and external parties."""
    
    TECHNOLOGY = "TECHNOLOGY"
    SERVICE = "SERVICE"
    CONSULTING = "CONSULTING"
    OUTSOURCING = "OUTSOURCING"
    CLOUD = "CLOUD"
    SUPPORT = "SUPPORT"
    SUPPLIER = "SUPPLIER"


class Policy(BaseAsset):
    """
    Policy model representing organizational policies and procedures.
    """
    
    # Policy classification
    policy_type: PolicyType = PolicyType.OPERATIONAL
    status: PolicyStatus = PolicyStatus.DRAFT
    
    # Policy metadata
    policy_number: Optional[str] = Field(None, description="Official policy number")
    policy_version: str = Field("1.0", description="Policy version")
    
    # Approval and authority
    approved_by: Optional[str] = Field(None, description="Who approved this policy")
    approved_at: Optional[datetime] = Field(None, description="When policy was approved")
    effective_date: Optional[datetime] = Field(None, description="When policy becomes effective")
    review_date: Optional[datetime] = Field(None, description="Next review date")
    expiry_date: Optional[datetime] = Field(None, description="Policy expiry date")
    
    # Policy content
    purpose: Optional[str] = Field(None, max_length=1000, description="Policy purpose")
    scope: Optional[str] = Field(None, max_length=1000, description="Policy scope")
    policy_text: Optional[str] = Field(None, description="Full policy text")
    
    # Compliance frameworks
    frameworks: List[str] = Field(default_factory=list, description="Compliance frameworks (GDPR, SOX, etc.)")
    regulations: List[str] = Field(default_factory=list, description="Applicable regulations")
    
    # Implementation
    mandatory: bool = Field(True, description="Whether policy compliance is mandatory")
    enforcement_level: Optional[str] = Field(None, description="Enforcement level")
    exceptions_allowed: bool = Field(False, description="Whether exceptions are allowed")
    
    # Documentation
    document_url: Optional[HttpUrl] = Field(None, description="Link to full policy document")
    training_required: bool = Field(False, description="Whether training is required")
    
    model_config = ConfigDict(use_enum_values=True)
    
    def __str__(self) -> str:
        """String representation."""
        return f"Policy: {self.name} ({self.policy_type})"
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"Policy(id='{self.id}', name='{self.name}', type='{self.policy_type}')"


class Risk(BaseAsset):
    """
    Risk model representing identified risks and their management.
    """
    
    # Risk classification
    risk_level: RiskLevel = RiskLevel.MEDIUM
    status: RiskStatus = RiskStatus.IDENTIFIED
    
    # Risk assessment
    likelihood: Optional[int] = Field(None, ge=1, le=5, description="Likelihood score (1-5)")
    impact: Optional[int] = Field(None, ge=1, le=5, description="Impact score (1-5)")
    risk_score: Optional[float] = Field(None, description="Calculated risk score")
    
    # Risk details
    threat_source: Optional[str] = Field(None, description="Source of the threat")
    vulnerability: Optional[str] = Field(None, description="Vulnerability being exploited")
    threat_event: Optional[str] = Field(None, description="Description of threat event")
    
    # Impact analysis
    business_impact: Optional[str] = Field(None, description="Business impact description")
    financial_impact: Optional[float] = Field(None, description="Estimated financial impact")
    operational_impact: Optional[str] = Field(None, description="Operational impact description")
    
    # Risk management
    risk_owner: Optional[str] = Field(None, description="Risk owner ID")
    mitigation_strategy: Optional[str] = Field(None, description="Mitigation strategy")
    mitigation_controls: List[str] = Field(default_factory=list, description="Mitigation control IDs")
    
    # Timeline
    identified_date: datetime = Field(default_factory=datetime.utcnow)
    target_resolution: Optional[datetime] = Field(None, description="Target resolution date")
    last_assessment: Optional[datetime] = Field(None, description="Last risk assessment date")
    next_review: Optional[datetime] = Field(None, description="Next review date")
    
    # Residual risk
    residual_likelihood: Optional[int] = Field(None, ge=1, le=5, description="Residual likelihood after controls")
    residual_impact: Optional[int] = Field(None, ge=1, le=5, description="Residual impact after controls")
    residual_score: Optional[float] = Field(None, description="Residual risk score")
    
    model_config = ConfigDict(use_enum_values=True)
    
    def __str__(self) -> str:
        """String representation."""
        return f"Risk: {self.name} ({self.risk_level})"
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"Risk(id='{self.id}', name='{self.name}', level='{self.risk_level}')"


class Process(BaseAsset):
    """
    Process model representing business and operational processes.
    """
    
    # Process classification
    process_type: ProcessType = ProcessType.OPERATIONAL
    
    # Process metadata
    process_id: Optional[str] = Field(None, description="Official process ID")
    process_version: str = Field("1.0", description="Process version")
    
    # Process details
    purpose: Optional[str] = Field(None, max_length=1000, description="Process purpose")
    scope: Optional[str] = Field(None, max_length=1000, description="Process scope")
    inputs: List[str] = Field(default_factory=list, description="Process inputs")
    outputs: List[str] = Field(default_factory=list, description="Process outputs")
    
    # Process ownership
    process_owner: Optional[str] = Field(None, description="Process owner ID")
    stakeholders: List[str] = Field(default_factory=list, description="Stakeholder IDs")
    
    # Process execution
    frequency: Optional[str] = Field(None, description="How often process runs")
    duration: Optional[str] = Field(None, description="Typical process duration")
    automation_level: Optional[str] = Field(None, description="Level of automation")
    
    # Quality and metrics
    kpis: List[str] = Field(default_factory=list, description="Key performance indicators")
    sla_targets: Dict[str, Any] = Field(default_factory=dict, description="SLA targets")
    
    # Documentation
    procedure_url: Optional[HttpUrl] = Field(None, description="Link to procedure document")
    flowchart_url: Optional[HttpUrl] = Field(None, description="Link to process flowchart")
    
    # Compliance
    regulatory_requirements: List[str] = Field(default_factory=list, description="Regulatory requirements")
    controls: List[str] = Field(default_factory=list, description="Associated control IDs")
    
    # Review and improvement
    last_review: Optional[datetime] = Field(None, description="Last process review date")
    next_review: Optional[datetime] = Field(None, description="Next review date")
    improvement_opportunities: List[str] = Field(default_factory=list, description="Improvement opportunities")
    
    model_config = ConfigDict(use_enum_values=True)
    
    def __str__(self) -> str:
        """String representation."""
        return f"Process: {self.name} ({self.process_type})"
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"Process(id='{self.id}', name='{self.name}', type='{self.process_type}')"


class Control(BaseAsset):
    """
    Control model representing security and compliance controls.
    """
    
    # Control classification
    control_type: ControlType = ControlType.PREVENTIVE
    control_id: Optional[str] = Field(None, description="Official control ID")
    
    # Control details
    objective: Optional[str] = Field(None, max_length=1000, description="Control objective")
    description_text: Optional[str] = Field(None, description="Detailed control description")
    
    # Implementation
    implementation_guidance: Optional[str] = Field(None, description="Implementation guidance")
    testing_procedures: Optional[str] = Field(None, description="Testing procedures")
    
    # Control effectiveness
    is_automated: bool = Field(False, description="Whether control is automated")
    effectiveness_rating: Optional[str] = Field(None, description="Control effectiveness rating")
    
    # Compliance mapping
    frameworks: List[str] = Field(default_factory=list, description="Compliance frameworks")
    control_families: List[str] = Field(default_factory=list, description="Control families")
    
    # Testing and validation
    test_frequency: Optional[str] = Field(None, description="How often control is tested")
    last_test_date: Optional[datetime] = Field(None, description="Last test date")
    next_test_date: Optional[datetime] = Field(None, description="Next test date")
    test_results: Optional[str] = Field(None, description="Latest test results")
    
    # Ownership and responsibility
    control_owner: Optional[str] = Field(None, description="Control owner ID")
    responsible_party: Optional[str] = Field(None, description="Responsible party ID")
    
    model_config = ConfigDict(use_enum_values=True)
    
    def __str__(self) -> str:
        """String representation."""
        return f"Control: {self.name} ({self.control_type})"


class Vendor(BaseAsset):
    """
    Vendor model representing external parties and service providers.
    """
    
    # Vendor classification
    vendor_type: VendorType = VendorType.SERVICE
    
    # Vendor details
    legal_name: str = Field(..., description="Legal business name")
    trading_name: Optional[str] = Field(None, description="Trading or DBA name")
    registration_number: Optional[str] = Field(None, description="Business registration number")
    tax_id: Optional[str] = Field(None, description="Tax identification number")
    
    # Contact information
    primary_contact: Optional[str] = Field(None, description="Primary contact person")
    email: Optional[str] = Field(None, description="Primary email address")
    phone: Optional[str] = Field(None, description="Primary phone number")
    website: Optional[HttpUrl] = Field(None, description="Vendor website")
    
    # Address information
    address: Optional[str] = Field(None, description="Business address")
    city: Optional[str] = Field(None, description="City")
    country: Optional[str] = Field(None, description="Country")
    
    # Business relationship
    relationship_start: Optional[datetime] = Field(None, description="Start of business relationship")
    relationship_status: Optional[str] = Field(None, description="Current relationship status")
    
    # Services and capabilities
    services_provided: List[str] = Field(default_factory=list, description="Services provided")
    capabilities: List[str] = Field(default_factory=list, description="Vendor capabilities")
    
    # Risk and compliance
    risk_rating: Optional[str] = Field(None, description="Vendor risk rating")
    compliance_certifications: List[str] = Field(default_factory=list, description="Compliance certifications")
    security_assessments: List[str] = Field(default_factory=list, description="Security assessment results")
    
    # Financial information
    annual_spend: Optional[float] = Field(None, ge=0, description="Annual spend with vendor")
    payment_terms: Optional[str] = Field(None, description="Payment terms")
    
    # Performance metrics
    sla_compliance: Optional[float] = Field(None, ge=0, le=100, description="SLA compliance percentage")
    performance_rating: Optional[str] = Field(None, description="Overall performance rating")
    
    model_config = ConfigDict(use_enum_values=True)
    
    def __str__(self) -> str:
        """String representation."""
        return f"Vendor: {self.legal_name} ({self.vendor_type})"
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"Vendor(id='{self.id}', name='{self.legal_name}', type='{self.vendor_type}')"


class Contract(BaseAsset):
    """
    Contract model representing agreements and SLAs.
    """
    
    # Contract details
    contract_number: Optional[str] = Field(None, description="Contract reference number")
    contract_type: Optional[str] = Field(None, description="Type of contract")
    
    # Parties
    vendor_id: Optional[str] = Field(None, description="Vendor ID")
    internal_owner: Optional[str] = Field(None, description="Internal contract owner")
    
    # Timeline
    effective_date: Optional[datetime] = Field(None, description="Contract effective date")
    expiry_date: Optional[datetime] = Field(None, description="Contract expiry date")
    notice_period: Optional[str] = Field(None, description="Termination notice period")
    
    # Financial terms
    contract_value: Optional[float] = Field(None, ge=0, description="Total contract value")
    payment_schedule: Optional[str] = Field(None, description="Payment schedule")
    currency: Optional[str] = Field(None, description="Contract currency")
    
    # Service levels
    sla_terms: Dict[str, Any] = Field(default_factory=dict, description="SLA terms and targets")
    penalties: Dict[str, Any] = Field(default_factory=dict, description="Penalty clauses")
    
    # Documentation
    contract_url: Optional[HttpUrl] = Field(None, description="Link to contract document")
    
    # Auto-renewal
    auto_renewal: bool = Field(False, description="Whether contract auto-renews")
    renewal_period: Optional[str] = Field(None, description="Auto-renewal period")
    
    model_config = ConfigDict()
    
    def __str__(self) -> str:
        """String representation."""
        return f"Contract: {self.name} ({self.contract_number or self.id})"