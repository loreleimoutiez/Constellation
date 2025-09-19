"""
Human asset models for people, teams, and organizational structures.

This module defines models for tracking human resources, organizational
units, roles, and skills within the CMDB.
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime, time

from pydantic import Field, EmailStr, ConfigDict

from .base import BaseAsset, TimestampMixin


class EmploymentStatus(str, Enum):
    """Employment status types."""
    
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    CONTRACTOR = "CONTRACTOR"
    CONSULTANT = "CONSULTANT"
    INTERN = "INTERN"
    FORMER = "FORMER"


class RoleType(str, Enum):
    """Types of roles within the organization."""
    
    TECHNICAL = "TECHNICAL"
    MANAGEMENT = "MANAGEMENT"
    BUSINESS = "BUSINESS"
    GOVERNANCE = "GOVERNANCE"
    SECURITY = "SECURITY"
    SUPPORT = "SUPPORT"


class SkillLevel(str, Enum):
    """Skill proficiency levels."""
    
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"


class TeamType(str, Enum):
    """Types of teams."""
    
    DEVELOPMENT = "DEVELOPMENT"
    OPERATIONS = "OPERATIONS"
    DEVOPS = "DEVOPS"
    SECURITY = "SECURITY"
    BUSINESS = "BUSINESS"
    MANAGEMENT = "MANAGEMENT"
    PROJECT = "PROJECT"
    VIRTUAL = "VIRTUAL"


class HumanAsset(BaseAsset):
    """
    Human asset model representing people in the organization.
    
    Stores essential information about individuals while respecting
    privacy and data protection requirements.
    """
    
    # Basic identification
    employee_id: Optional[str] = Field(None, description="Employee ID or badge number")
    email: Optional[EmailStr] = Field(None, description="Primary email address")
    display_name: Optional[str] = Field(None, description="Preferred display name")
    
    # Employment information
    employment_status: EmploymentStatus = EmploymentStatus.ACTIVE
    hire_date: Optional[datetime] = Field(None, description="Date of hire")
    termination_date: Optional[datetime] = Field(None, description="Date of termination if applicable")
    
    # Organizational placement
    department: Optional[str] = Field(None, description="Department or division")
    cost_center: Optional[str] = Field(None, description="Cost center code")
    location: Optional[str] = Field(None, description="Primary work location")
    
    # Contact information (work-related only)
    phone: Optional[str] = Field(None, description="Work phone number")
    office: Optional[str] = Field(None, description="Office location or room number")
    
    # Operational details
    manager_id: Optional[str] = Field(None, description="ID of direct manager")
    is_manager: bool = Field(False, description="Whether this person manages others")
    
    # On-call and availability
    on_call_enabled: bool = Field(False, description="Whether person is in on-call rotation")
    working_hours_start: Optional[time] = Field(None, description="Normal working hours start")
    working_hours_end: Optional[time] = Field(None, description="Normal working hours end")
    timezone: Optional[str] = Field(None, description="Primary timezone")
    
    # System access and security
    security_clearance: Optional[str] = Field(None, description="Security clearance level")
    access_level: Optional[str] = Field(None, description="System access level")
    
    # Flexible attributes
    custom_attributes: Dict[str, Any] = Field(default_factory=dict, description="Custom attributes")
    
    model_config = ConfigDict(use_enum_values=True)
    
    def __str__(self) -> str:
        """String representation."""
        return f"Human: {self.display_name or self.name} ({self.employee_id or self.id})"
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"HumanAsset(id='{self.id}', name='{self.name}', status='{self.employment_status}')"


class Skill(TimestampMixin):
    """
    Skill model representing competencies and expertise.
    """
    
    # Core skill definition
    name: str = Field(..., min_length=1, max_length=100, description="Skill name")
    category: Optional[str] = Field(None, description="Skill category (e.g., 'Programming', 'Networking')")
    description: Optional[str] = Field(None, max_length=500, description="Skill description")
    
    # Skill metadata
    is_technical: bool = Field(True, description="Whether this is a technical skill")
    is_certification: bool = Field(False, description="Whether this represents a certification")
    
    # Certification details
    certification_authority: Optional[str] = Field(None, description="Certifying body")
    certification_id: Optional[str] = Field(None, description="Certification ID or number")
    expires_at: Optional[datetime] = Field(None, description="Certification expiry date")
    
    model_config = ConfigDict()


class Role(BaseAsset):
    """
    Role model representing organizational roles and positions.
    """
    
    # Role definition
    role_type: RoleType = RoleType.TECHNICAL
    level: Optional[str] = Field(None, description="Role level (e.g., 'Senior', 'Lead', 'Principal')")
    
    # Organizational context
    department: Optional[str] = Field(None, description="Department this role belongs to")
    team_id: Optional[str] = Field(None, description="Primary team for this role")
    reports_to_role_id: Optional[str] = Field(None, description="Role this position reports to")
    
    # Role characteristics
    is_management_role: bool = Field(False, description="Whether this is a management role")
    is_on_call_role: bool = Field(False, description="Whether this role includes on-call duties")
    requires_security_clearance: bool = Field(False, description="Whether role requires security clearance")
    
    # Responsibilities and permissions
    responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities")
    required_skills: List[str] = Field(default_factory=list, description="Required skill names")
    preferred_skills: List[str] = Field(default_factory=list, description="Preferred skill names")
    
    # Operational details
    headcount: int = Field(1, ge=1, description="Number of people in this role")
    is_active: bool = Field(True, description="Whether role is currently active")
    
    model_config = ConfigDict(use_enum_values=True)
    
    def __str__(self) -> str:
        """String representation."""
        return f"Role: {self.name} ({self.role_type})"
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"Role(id='{self.id}', name='{self.name}', type='{self.role_type}')"


class Team(BaseAsset):
    """
    Team model representing organizational units and groups.
    """
    
    # Team definition
    team_type: TeamType = TeamType.DEVELOPMENT
    
    # Organizational hierarchy
    parent_team_id: Optional[str] = Field(None, description="Parent team ID")
    department: Optional[str] = Field(None, description="Department this team belongs to")
    
    # Team leadership
    team_lead_id: Optional[str] = Field(None, description="Team lead person ID")
    manager_id: Optional[str] = Field(None, description="Team manager person ID")
    
    # Team characteristics
    is_virtual: bool = Field(False, description="Whether this is a virtual/cross-functional team")
    is_temporary: bool = Field(False, description="Whether this is a temporary team")
    
    # Contact and location
    primary_location: Optional[str] = Field(None, description="Primary team location")
    contact_email: Optional[EmailStr] = Field(None, description="Team contact email")
    slack_channel: Optional[str] = Field(None, description="Slack channel name")
    
    # Operational details
    budget_code: Optional[str] = Field(None, description="Budget or cost center code")
    max_size: Optional[int] = Field(None, ge=1, description="Maximum team size")
    
    # Team metrics and goals
    objectives: List[str] = Field(default_factory=list, description="Team objectives")
    key_metrics: Dict[str, Any] = Field(default_factory=dict, description="Key performance metrics")
    
    model_config = ConfigDict(use_enum_values=True)
    
    def __str__(self) -> str:
        """String representation."""
        return f"Team: {self.name} ({self.team_type})"
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"Team(id='{self.id}', name='{self.name}', type='{self.team_type}')"


class HumanSkillRelation(TimestampMixin):
    """
    Relationship between a human and a skill, including proficiency level.
    """
    
    human_id: str = Field(..., description="Human asset ID")
    skill_name: str = Field(..., description="Skill name")
    level: SkillLevel = SkillLevel.INTERMEDIATE
    
    # Verification and evidence
    verified: bool = Field(False, description="Whether skill level has been verified")
    verified_by: Optional[str] = Field(None, description="Who verified this skill")
    verified_at: Optional[datetime] = Field(None, description="When skill was verified")
    
    # Skill acquisition
    acquired_at: Optional[datetime] = Field(None, description="When skill was acquired")
    years_experience: Optional[float] = Field(None, ge=0, description="Years of experience")
    
    # Evidence and documentation
    evidence_type: Optional[str] = Field(None, description="Type of evidence (certification, project, etc.)")
    evidence_ref: Optional[str] = Field(None, description="Reference to evidence")
    
    model_config = ConfigDict(use_enum_values=True)
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.human_id} has {self.skill_name} at {self.level} level"