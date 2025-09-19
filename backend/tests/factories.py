"""
Test factories for creating model instances with sensible defaults.

This module provides factory functions to create model instances for testing
with all required fields populated and sensible defaults.
"""

from datetime import datetime, time
from typing import Optional, Dict, Any

from app.models.base import BaseAsset, CriticalityLevel, EnvironmentType, LifecycleState
from app.models.ci import CI, CIType
from app.models.human import (
    HumanAsset, Team, Role, Skill, HumanSkillRelation,
    EmploymentStatus, RoleType, SkillLevel, TeamType
)


# BaseAsset Factory
def create_base_asset(
    name: str = "Test Asset",
    description: str = "Test asset description",
    owner: str = "test-owner",
    confidentiality: str = "internal",
    integrity: str = "standard",
    availability: str = "standard",
    pii: bool = False,
    version: str = "1.0",
    evidence_ref: str = "test-evidence",
    **kwargs
) -> BaseAsset:
    """Create a BaseAsset with sensible defaults."""
    return BaseAsset(
        name=name,
        description=description,
        owner=owner,
        confidentiality=confidentiality,
        integrity=integrity,
        availability=availability,
        pii=pii,
        version=version,
        evidence_ref=evidence_ref,
        **kwargs
    )


# CI Factory
def create_ci(
    name: str = "Test CI",
    description: str = "Test CI description",
    owner: str = "test-owner",
    confidentiality: str = "internal",
    integrity: str = "standard",
    availability: str = "standard",
    pii: bool = False,
    version: str = "1.0",
    evidence_ref: str = "test-evidence",
    ci_type: CIType = CIType.GENERIC,
    hostname: Optional[str] = None,
    ip_address: Optional[str] = None,
    fqdn: Optional[str] = None,
    vendor: Optional[str] = None,
    model: Optional[str] = None,
    serial_number: Optional[str] = None,
    asset_tag: Optional[str] = None,
    location: Optional[str] = None,
    rack_position: Optional[str] = None,
    status: Optional[str] = "active",
    monitoring_enabled: bool = True,
    backup_enabled: bool = False,
    cost_center: Optional[str] = None,
    **kwargs
) -> CI:
    """Create a CI with sensible defaults."""
    return CI(
        name=name,
        description=description,
        owner=owner,
        confidentiality=confidentiality,
        integrity=integrity,
        availability=availability,
        pii=pii,
        version=version,
        evidence_ref=evidence_ref,
        ci_type=ci_type,
        hostname=hostname,
        ip_address=ip_address,
        fqdn=fqdn,
        vendor=vendor,
        model=model,
        serial_number=serial_number,
        asset_tag=asset_tag,
        location=location,
        rack_position=rack_position,
        status=status,
        monitoring_enabled=monitoring_enabled,
        backup_enabled=backup_enabled,
        cost_center=cost_center,
        **kwargs
    )


# HumanAsset Factory
def create_human_asset(
    name: str = "John Doe",
    description: str = "Test employee",
    owner: str = "hr-department",
    confidentiality: str = "restricted",
    integrity: str = "high",
    availability: str = "standard",
    pii: bool = True,
    version: str = "1.0",
    evidence_ref: str = "hr-record",
    employee_id: str = "EMP001",
    email: str = "john.doe@company.com",
    display_name: str = "John Doe",
    hire_date: Optional[datetime] = None,
    termination_date: Optional[datetime] = None,
    department: str = "Engineering",
    cost_center: str = "ENG-001",
    location: str = "HQ-Building-A",
    phone: str = "+1-555-0123",
    office: str = "A-301",
    manager_id: Optional[str] = None,
    is_manager: bool = False,
    on_call_enabled: bool = False,
    working_hours_start: time = time(9, 0),
    working_hours_end: time = time(17, 0),
    timezone: str = "UTC",
    security_clearance: Optional[str] = None,
    access_level: str = "standard",
    **kwargs
) -> HumanAsset:
    """Create a HumanAsset with sensible defaults."""
    if hire_date is None:
        hire_date = datetime(2020, 1, 1)
    
    return HumanAsset(
        name=name,
        description=description,
        owner=owner,
        confidentiality=confidentiality,
        integrity=integrity,
        availability=availability,
        pii=pii,
        version=version,
        evidence_ref=evidence_ref,
        employee_id=employee_id,
        email=email,
        display_name=display_name,
        hire_date=hire_date,
        termination_date=termination_date,
        department=department,
        cost_center=cost_center,
        location=location,
        phone=phone,
        office=office,
        manager_id=manager_id,
        is_manager=is_manager,
        on_call_enabled=on_call_enabled,
        working_hours_start=working_hours_start,
        working_hours_end=working_hours_end,
        timezone=timezone,
        security_clearance=security_clearance,
        access_level=access_level,
        **kwargs
    )


# Team Factory
def create_team(
    name: str = "Test Team",
    description: str = "Test team description",
    owner: str = "team-lead",
    confidentiality: str = "internal",
    integrity: str = "standard",
    availability: str = "standard",
    pii: bool = False,
    version: str = "1.0",
    evidence_ref: str = "org-chart",
    parent_team_id: Optional[str] = None,
    department: str = "Engineering",
    team_lead_id: Optional[str] = None,
    manager_id: Optional[str] = None,
    is_virtual: bool = False,
    is_temporary: bool = False,
    primary_location: str = "HQ",
    contact_email: str = "team@company.com",
    slack_channel: Optional[str] = None,
    budget_code: Optional[str] = None,
    max_size: int = 10,
    **kwargs
) -> Team:
    """Create a Team with sensible defaults."""
    return Team(
        name=name,
        description=description,
        owner=owner,
        confidentiality=confidentiality,
        integrity=integrity,
        availability=availability,
        pii=pii,
        version=version,
        evidence_ref=evidence_ref,
        parent_team_id=parent_team_id,
        department=department,
        team_lead_id=team_lead_id,
        manager_id=manager_id,
        is_virtual=is_virtual,
        is_temporary=is_temporary,
        primary_location=primary_location,
        contact_email=contact_email,
        slack_channel=slack_channel,
        budget_code=budget_code,
        max_size=max_size,
        **kwargs
    )


# Role Factory
def create_role(
    name: str = "Software Engineer",
    description: str = "Test role description",
    owner: str = "hr-department",
    confidentiality: str = "internal",
    integrity: str = "standard",
    availability: str = "standard",
    pii: bool = False,
    version: str = "1.0",
    evidence_ref: str = "job-description",
    level: str = "Mid",
    department: str = "Engineering",
    team_id: Optional[str] = None,
    reports_to_role_id: Optional[str] = None,
    is_management_role: bool = False,
    is_on_call_role: bool = False,
    requires_security_clearance: bool = False,
    headcount: int = 1,
    is_active: bool = True,
    **kwargs
) -> Role:
    """Create a Role with sensible defaults."""
    return Role(
        name=name,
        description=description,
        owner=owner,
        confidentiality=confidentiality,
        integrity=integrity,
        availability=availability,
        pii=pii,
        version=version,
        evidence_ref=evidence_ref,
        level=level,
        department=department,
        team_id=team_id,
        reports_to_role_id=reports_to_role_id,
        is_management_role=is_management_role,
        is_on_call_role=is_on_call_role,
        requires_security_clearance=requires_security_clearance,
        headcount=headcount,
        is_active=is_active,
        **kwargs
    )


# Skill Factory
def create_skill(
    name: str = "Python",
    category: str = "Programming Language",
    description: str = "Test skill description",
    is_technical: bool = True,
    is_certification: bool = False,
    certification_authority: Optional[str] = None,
    certification_id: Optional[str] = None,
    expires_at: Optional[datetime] = None,
    **kwargs
) -> Skill:
    """Create a Skill with sensible defaults."""
    return Skill(
        name=name,
        category=category,
        description=description,
        is_technical=is_technical,
        is_certification=is_certification,
        certification_authority=certification_authority,
        certification_id=certification_id,
        expires_at=expires_at,
        **kwargs
    )


# HumanSkillRelation Factory
def create_human_skill_relation(
    human_id: str = "human-123",
    skill_name: str = "Python",
    verified: bool = False,
    verified_by: Optional[str] = None,
    verified_at: Optional[datetime] = None,
    acquired_at: Optional[datetime] = None,
    years_experience: float = 1.0,
    evidence_type: str = "self-reported",
    evidence_ref: str = "test-evidence",
    **kwargs
) -> HumanSkillRelation:
    """Create a HumanSkillRelation with sensible defaults."""
    if acquired_at is None:
        acquired_at = datetime(2020, 1, 1)
    
    return HumanSkillRelation(
        human_id=human_id,
        skill_name=skill_name,
        verified=verified,
        verified_by=verified_by,
        verified_at=verified_at,
        acquired_at=acquired_at,
        years_experience=years_experience,
        evidence_type=evidence_type,
        evidence_ref=evidence_ref,
        **kwargs
    )


# Relationship Factory
def create_relationship(
    source_id: str = "asset-source-123",
    target_id: str = "asset-target-456", 
    relationship_type = None,
    weight: float = 1.0,
    description: str = "Test relationship",
    active: bool = True,
    verified: bool = False,
    auto_discovered: bool = False,
    conditions: Optional[str] = None,
    port: Optional[str] = None,
    protocol: Optional[str] = None,
    discovered_by: Optional[str] = None,
    discovered_at: Optional[datetime] = None,
    last_verified: Optional[datetime] = None,
    **kwargs
):
    """Create a Relationship with sensible defaults."""
    from app.models.relationships import Relationship, RelationshipType
    
    if relationship_type is None:
        relationship_type = RelationshipType.DEPENDS_ON
    
    return Relationship(
        source_id=source_id,
        target_id=target_id,
        relationship_type=relationship_type,
        weight=weight,
        description=description,
        active=active,
        verified=verified,
        auto_discovered=auto_discovered,
        conditions=conditions,
        port=port,
        protocol=protocol,
        discovered_by=discovered_by,
        discovered_at=discovered_at,
        last_verified=last_verified,
        **kwargs
    )