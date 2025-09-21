"""
Tests for human asset models (HumanAsset, Team, Role, Skill).
"""

import pytest
from datetime import datetime, time
from uuid import UUID

from app.models.human import (
    HumanAsset,
    Team,
    Role,
    Skill,
    HumanSkillRelation,
    EmploymentStatus,
    RoleType,
    SkillLevel,
    TeamType,
)
from tests.factories import (
    create_human_asset,
    create_team,
    create_role,
    create_skill,
    create_human_skill_relation,
)


class TestEmploymentStatus:
    """Test EmploymentStatus enum."""

    def test_employment_status_values(self):
        """Test all employment status values."""
        assert EmploymentStatus.ACTIVE == "ACTIVE"
        assert EmploymentStatus.INACTIVE == "INACTIVE"
        assert EmploymentStatus.CONTRACTOR == "CONTRACTOR"
        assert EmploymentStatus.CONSULTANT == "CONSULTANT"
        assert EmploymentStatus.INTERN == "INTERN"
        assert EmploymentStatus.FORMER == "FORMER"


class TestRoleType:
    """Test RoleType enum."""

    def test_role_type_values(self):
        """Test all role type values."""
        assert RoleType.TECHNICAL == "TECHNICAL"
        assert RoleType.MANAGEMENT == "MANAGEMENT"
        assert RoleType.BUSINESS == "BUSINESS"
        assert RoleType.GOVERNANCE == "GOVERNANCE"
        assert RoleType.SECURITY == "SECURITY"
        assert RoleType.SUPPORT == "SUPPORT"


class TestSkillLevel:
    """Test SkillLevel enum."""

    def test_skill_level_values(self):
        """Test all skill level values."""
        assert SkillLevel.BEGINNER == "BEGINNER"
        assert SkillLevel.INTERMEDIATE == "INTERMEDIATE"
        assert SkillLevel.ADVANCED == "ADVANCED"
        assert SkillLevel.EXPERT == "EXPERT"


class TestTeamType:
    """Test TeamType enum."""

    def test_team_type_values(self):
        """Test all team type values."""
        assert TeamType.DEVELOPMENT == "DEVELOPMENT"
        assert TeamType.OPERATIONS == "OPERATIONS"
        assert TeamType.DEVOPS == "DEVOPS"
        assert TeamType.SECURITY == "SECURITY"
        assert TeamType.BUSINESS == "BUSINESS"
        assert TeamType.MANAGEMENT == "MANAGEMENT"
        assert TeamType.PROJECT == "PROJECT"
        assert TeamType.VIRTUAL == "VIRTUAL"


class TestHumanAsset:
    """Test HumanAsset model."""

    def test_human_asset_creation_minimal(self):
        """Test creating HumanAsset with minimal required fields."""
        human = create_human_asset(name="John Doe")

        # Check required fields
        assert human.name == "John Doe"

        # Check defaults
        assert human.employment_status == EmploymentStatus.ACTIVE
        assert human.is_manager is False
        assert human.on_call_enabled is False
        assert human.custom_attributes == {}

        # Check inherited from BaseAsset
        assert isinstance(UUID(human.id), UUID)
        assert human.pii is True  # Human assets contain PII by default

    def test_human_asset_creation_full(self):
        """Test creating HumanAsset with all fields."""
        hire_date = datetime(2023, 1, 15)
        start_time = time(9, 0)
        end_time = time(17, 30)

        human = create_human_asset(
            name="Jane Smith",
            employee_id="EMP001",
            email="jane.smith@company.com",
            display_name="Jane",
            employment_status=EmploymentStatus.ACTIVE,
            hire_date=hire_date,
            department="Engineering",
            cost_center="ENG-001",
            location="New York Office",
            phone="+1-555-0123",
            office="Floor 3, Room 301",
            is_manager=True,
            on_call_enabled=True,
            working_hours_start=start_time,
            working_hours_end=end_time,
            timezone="America/New_York",
            security_clearance="SECRET",
            access_level="ADMIN",
        )

        # Verify all fields are set correctly
        assert human.name == "Jane Smith"
        assert human.employee_id == "EMP001"
        assert human.email == "jane.smith@company.com"
        assert human.display_name == "Jane"
        assert human.employment_status == EmploymentStatus.ACTIVE
        assert human.hire_date == hire_date
        assert human.department == "Engineering"
        assert human.is_manager is True
        assert human.on_call_enabled is True
        assert human.working_hours_start == start_time
        assert human.working_hours_end == end_time
        assert human.timezone == "America/New_York"

    def test_human_asset_with_manager(self):
        """Test HumanAsset with manager relationship."""
        manager_id = "mgr-123"

        human = create_human_asset(name="Report Employee", manager_id=manager_id)

        assert human.manager_id == manager_id
        assert human.is_manager is False

    def test_human_asset_contractor(self):
        """Test HumanAsset for contractor."""
        termination_date = datetime(2025, 12, 31)

        contractor = create_human_asset(
            name="External Contractor",
            employment_status=EmploymentStatus.CONTRACTOR,
            termination_date=termination_date,
        )

        assert contractor.employment_status == EmploymentStatus.CONTRACTOR
        assert contractor.termination_date == termination_date

    def test_human_asset_string_representations(self):
        """Test HumanAsset string and repr methods."""
        human = create_human_asset(
            name="John Doe", employee_id="EMP001", display_name="John"
        )

        # Test __str__ method
        str_repr = str(human)
        assert "Human: John (EMP001)" == str_repr

        # Test __repr__ method
        repr_str = repr(human)
        assert "HumanAsset(" in repr_str
        assert "name='John Doe'" in repr_str
        assert (
            "status='EmploymentStatus.ACTIVE'" in repr_str
            or "status='ACTIVE'" in repr_str
        )

    def test_human_asset_json_serialization(self):
        """Test HumanAsset JSON serialization."""
        human = create_human_asset(
            name="Test User",
            email="test@company.com",
            employment_status=EmploymentStatus.ACTIVE,
        )

        json_data = human.model_dump()

        assert json_data["name"] == "Test User"
        assert json_data["email"] == "test@company.com"
        assert json_data["employment_status"] == "ACTIVE"
        assert "id" in json_data
        assert "created_at" in json_data


class TestTeam:
    """Test Team model."""

    def test_team_creation_minimal(self):
        """Test creating Team with minimal required fields."""
        team = create_team(name="DevOps Team")

        # Check required fields
        assert team.name == "DevOps Team"

        # Check defaults
        assert team.team_type == TeamType.DEVELOPMENT
        assert team.is_virtual is False
        assert team.is_temporary is False
        assert team.objectives == []
        assert team.key_metrics == {}

        # Check inherited from BaseAsset
        assert isinstance(UUID(team.id), UUID)

    def test_team_creation_full(self):
        """Test creating Team with all fields."""
        objectives = ["Improve deployment speed", "Reduce downtime"]
        metrics = {"deployment_frequency": "daily", "mttr_hours": 2}

        team = create_team(
            name="Platform Engineering",
            team_type=TeamType.DEVOPS,
            department="Engineering",
            team_lead_id="lead-123",
            manager_id="mgr-456",
            is_virtual=False,
            primary_location="San Francisco",
            contact_email="platform@company.com",
            slack_channel="#platform-team",
            budget_code="ENG-PLATFORM",
            max_size=12,
            objectives=objectives,
            key_metrics=metrics,
        )

        # Verify all fields are set correctly
        assert team.name == "Platform Engineering"
        assert team.team_type == TeamType.DEVOPS
        assert team.department == "Engineering"
        assert team.team_lead_id == "lead-123"
        assert team.manager_id == "mgr-456"
        assert team.primary_location == "San Francisco"
        assert team.contact_email == "platform@company.com"
        assert team.slack_channel == "#platform-team"
        assert team.max_size == 12
        assert team.objectives == objectives
        assert team.key_metrics == metrics

    def test_team_hierarchy(self):
        """Test Team with parent-child relationships."""
        parent_team_id = "parent-team-123"

        child_team = create_team(
            name="Frontend Team",
            team_type=TeamType.DEVELOPMENT,
            parent_team_id=parent_team_id,
        )

        assert child_team.parent_team_id == parent_team_id

    def test_team_virtual_and_temporary(self):
        """Test virtual and temporary team flags."""
        team = create_team(
            name="Project Alpha",
            team_type=TeamType.PROJECT,
            is_virtual=True,
            is_temporary=True,
        )

        assert team.is_virtual is True
        assert team.is_temporary is True

    def test_team_string_representations(self):
        """Test Team string and repr methods."""
        team = create_team(name="Security Team", team_type=TeamType.SECURITY)

        # Test __str__ method
        str_repr = str(team)
        assert str_repr == "Team: Security Team (SECURITY)"

        # Test __repr__ method
        repr_str = repr(team)
        assert "Team(" in repr_str
        assert "name='Security Team'" in repr_str
        assert "type='SECURITY'" in repr_str


class TestRole:
    """Test Role model."""

    def test_role_creation_minimal(self):
        """Test creating Role with minimal required fields."""
        role = create_role(name="Software Engineer")

        # Check required fields
        assert role.name == "Software Engineer"

        # Check defaults
        assert role.role_type == RoleType.TECHNICAL
        assert role.is_management_role is False
        assert role.is_on_call_role is False
        assert role.requires_security_clearance is False
        assert role.responsibilities == []
        assert role.required_skills == []
        assert role.preferred_skills == []
        assert role.headcount == 1
        assert role.is_active is True

    def test_role_creation_full(self):
        """Test creating Role with all fields."""
        responsibilities = ["Code development", "Code review", "Mentoring"]
        required_skills = ["Python", "FastAPI", "PostgreSQL"]
        preferred_skills = ["Neo4j", "Docker", "Kubernetes"]

        role = create_role(
            name="Senior Software Engineer",
            role_type=RoleType.TECHNICAL,
            level="Senior",
            department="Engineering",
            team_id="team-123",
            reports_to_role_id="tech-lead-role",
            is_management_role=False,
            is_on_call_role=True,
            requires_security_clearance=True,
            responsibilities=responsibilities,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            headcount=3,
        )

        # Verify all fields are set correctly
        assert role.name == "Senior Software Engineer"
        assert role.role_type == RoleType.TECHNICAL
        assert role.level == "Senior"
        assert role.department == "Engineering"
        assert role.team_id == "team-123"
        assert role.is_on_call_role is True
        assert role.requires_security_clearance is True
        assert role.responsibilities == responsibilities
        assert role.required_skills == required_skills
        assert role.preferred_skills == preferred_skills
        assert role.headcount == 3

    def test_role_management_role(self):
        """Test management role creation."""
        role = create_role(
            name="Engineering Manager",
            role_type=RoleType.MANAGEMENT,
            is_management_role=True,
            headcount=1,
        )

        assert role.role_type == RoleType.MANAGEMENT
        assert role.is_management_role is True

    def test_role_headcount_validation(self):
        """Test role headcount validation (must be >= 1)."""
        # Valid headcount
        role = create_role(name="Developer", headcount=5)
        assert role.headcount == 5

        # Invalid headcount - should fail during factory creation
        with pytest.raises(ValueError):
            create_role(name="Developer", headcount=0)

    def test_role_string_representations(self):
        """Test Role string and repr methods."""
        role = create_role(name="DevOps Engineer", role_type=RoleType.TECHNICAL)

        # Test __str__ method
        str_repr = str(role)
        assert str_repr == "Role: DevOps Engineer (TECHNICAL)"

        # Test __repr__ method
        repr_str = repr(role)
        assert "Role(" in repr_str
        assert "name='DevOps Engineer'" in repr_str
        assert "type='TECHNICAL'" in repr_str


class TestSkill:
    """Test Skill model."""

    def test_skill_creation_minimal(self):
        """Test creating Skill with minimal required fields."""
        skill = create_skill(name="Python")

        # Check required fields
        assert skill.name == "Python"

        # Check defaults
        assert skill.is_technical is True
        assert skill.is_certification is False

    def test_skill_creation_full(self):
        """Test creating Skill with all fields."""
        expiry_date = datetime(2026, 12, 31)

        skill = create_skill(
            name="AWS Solutions Architect",
            category="Cloud Computing",
            description="AWS Solutions Architect Professional certification",
            is_technical=True,
            is_certification=True,
            certification_authority="Amazon Web Services",
            certification_id="AWS-SAP-001234",
            expires_at=expiry_date,
        )

        # Verify all fields are set correctly
        assert skill.name == "AWS Solutions Architect"
        assert skill.category == "Cloud Computing"
        assert skill.is_certification is True
        assert skill.certification_authority == "Amazon Web Services"
        assert skill.certification_id == "AWS-SAP-001234"
        assert skill.expires_at == expiry_date

    def test_skill_technical_vs_soft(self):
        """Test technical vs soft skills."""
        technical_skill = create_skill(name="Kubernetes", is_technical=True)

        soft_skill = create_skill(name="Leadership", is_technical=False)

        assert technical_skill.is_technical is True
        assert soft_skill.is_technical is False


class TestHumanSkillRelation:
    """Test HumanSkillRelation model."""

    def test_human_skill_relation_minimal(self):
        """Test creating HumanSkillRelation with minimal fields."""
        relation = create_human_skill_relation(
            human_id="human-123", skill_name="Python"
        )

        # Check required fields
        assert relation.human_id == "human-123"
        assert relation.skill_name == "Python"

        # Check defaults
        assert relation.level == SkillLevel.INTERMEDIATE
        assert relation.verified is False

    def test_human_skill_relation_full(self):
        """Test creating HumanSkillRelation with all fields."""
        acquired_date = datetime(2020, 1, 1)
        verified_date = datetime(2025, 1, 1)

        relation = create_human_skill_relation(
            human_id="human-456",
            skill_name="Java",
            level=SkillLevel.EXPERT,
            verified=True,
            verified_by="tech-lead-789",
            verified_at=verified_date,
            acquired_at=acquired_date,
            years_experience=5.5,
            evidence_type="certification",
            evidence_ref="oracle-java-cert-001",
        )

        # Verify all fields are set correctly
        assert relation.human_id == "human-456"
        assert relation.skill_name == "Java"
        assert relation.level == SkillLevel.EXPERT
        assert relation.verified is True
        assert relation.verified_by == "tech-lead-789"
        assert relation.verified_at == verified_date
        assert relation.acquired_at == acquired_date
        assert relation.years_experience == 5.5
        assert relation.evidence_type == "certification"
        assert relation.evidence_ref == "oracle-java-cert-001"

    def test_human_skill_relation_years_validation(self):
        """Test years_experience validation (must be >= 0)."""
        # Valid years
        relation = create_human_skill_relation(
            human_id="human-123", skill_name="Python", years_experience=3.5
        )
        assert relation.years_experience == 3.5

        # Invalid years - should fail during factory creation
        with pytest.raises(ValueError):
            create_human_skill_relation(
                human_id="human-123", skill_name="Python", years_experience=-1.0
            )

    def test_human_skill_relation_string_representation(self):
        """Test HumanSkillRelation string representation."""
        relation = create_human_skill_relation(
            human_id="human-123", skill_name="Docker", level=SkillLevel.ADVANCED
        )

        str_repr = str(relation)
        assert str_repr == "human-123 has Docker at ADVANCED level"
