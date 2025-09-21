#!/usr/bin/env python3
"""
Script complet pour recréer tous les types d'assets et relations pour Constellation CMDB
Génère une base complète avec tous les types possibles et de nombreuses relations
"""

import requests
import json
import random
from datetime import datetime, timedelta
from faker import Faker
import time

fake = Faker("fr_FR")

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
TOTAL_ASSETS = 80
TOTAL_RELATIONS = 120

# Types d'assets étendus
ASSET_TEMPLATES = {
    # INFRASTRUCTURE TANGIBLE
    "servers": {
        "category": "tangible",
        "ci_type": "HARDWARE",
        "environments": ["PROD", "DEV", "TEST", "STAGING"],
        "criticalities": ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        "count": 15,
    },
    "workstations": {
        "category": "tangible",
        "ci_type": "ENDPOINT",
        "environments": ["PROD", "DEV"],
        "criticalities": ["MEDIUM", "LOW"],
        "count": 8,
    },
    "network_devices": {
        "category": "tangible",
        "ci_type": "NETWORK",
        "environments": ["PROD", "DEV"],
        "criticalities": ["CRITICAL", "HIGH", "MEDIUM"],
        "count": 6,
    },
    "storage_devices": {
        "category": "tangible",
        "ci_type": "STORAGE",
        "environments": ["PROD", "DEV", "TEST"],
        "criticalities": ["HIGH", "MEDIUM"],
        "count": 4,
    },
    # APPLICATIONS ET LOGICIELS
    "applications": {
        "category": "tangible",
        "ci_type": "APPLICATION",
        "environments": ["PROD", "DEV", "TEST"],
        "criticalities": ["CRITICAL", "HIGH", "MEDIUM"],
        "count": 12,
    },
    "system_software": {
        "category": "tangible",
        "ci_type": "SOFTWARE",
        "environments": ["PROD", "DEV", "TEST"],
        "criticalities": ["HIGH", "MEDIUM", "LOW"],
        "count": 8,
    },
    "middleware": {
        "category": "tangible",
        "ci_type": "MIDDLEWARE",
        "environments": ["PROD", "DEV", "TEST"],
        "criticalities": ["HIGH", "MEDIUM"],
        "count": 5,
    },
    # BASES DE DONNÉES ET SERVICES
    "databases": {
        "category": "tangible",
        "ci_type": "DATABASE",
        "environments": ["PROD", "DEV", "TEST"],
        "criticalities": ["CRITICAL", "HIGH", "MEDIUM"],
        "count": 8,
    },
    "services": {
        "category": "tangible",
        "ci_type": "SERVICE",
        "environments": ["PROD", "DEV", "TEST"],
        "criticalities": ["HIGH", "MEDIUM", "LOW"],
        "count": 6,
    },
    # RESSOURCES HUMAINES
    "employees": {
        "category": "intangible",
        "ci_type": "IDENTITY",
        "criticalities": ["HIGH", "MEDIUM", "LOW"],
        "count": 10,
        "intangible_type": "human",
    },
    "teams": {
        "category": "intangible",
        "ci_type": "IDENTITY",
        "criticalities": ["HIGH", "MEDIUM"],
        "count": 5,
        "intangible_type": "team",
    },
    "contractors": {
        "category": "intangible",
        "ci_type": "IDENTITY",
        "criticalities": ["MEDIUM", "LOW"],
        "count": 3,
        "intangible_type": "contractor",
    },
    # GOUVERNANCE ET DOCUMENTATION
    "policies": {
        "category": "intangible",
        "ci_type": "DATASET",
        "criticalities": ["HIGH", "MEDIUM"],
        "count": 4,
        "intangible_type": "governance",
    },
    "procedures": {
        "category": "intangible",
        "ci_type": "DATASET",
        "criticalities": ["MEDIUM", "LOW"],
        "count": 4,
        "intangible_type": "documentation",
    },
    "certifications": {
        "category": "intangible",
        "ci_type": "GENERIC",
        "criticalities": ["HIGH", "MEDIUM"],
        "count": 3,
        "intangible_type": "certification",
    },
    # LICENCES ET CONTRATS
    "software_licenses": {
        "category": "intangible",
        "ci_type": "GENERIC",
        "criticalities": ["HIGH", "MEDIUM"],
        "count": 6,
        "intangible_type": "license",
    },
    "contracts": {
        "category": "intangible",
        "ci_type": "GENERIC",
        "criticalities": ["HIGH", "MEDIUM"],
        "count": 3,
        "intangible_type": "contract",
    },
}

# Noms réalistes étendus
NAMES_BY_TYPE = {
    "servers": [
        "srv-web-prod-01",
        "srv-web-prod-02",
        "srv-app-dev-01",
        "srv-app-dev-02",
        "srv-db-prod-01",
        "srv-db-prod-02",
        "srv-backup-01",
        "srv-monitoring-01",
        "srv-file-share-01",
        "srv-mail-prod-01",
        "srv-dns-01",
        "srv-proxy-prod-01",
        "srv-jenkins-dev-01",
        "srv-gitlab-prod-01",
        "srv-elk-stack-01",
    ],
    "workstations": [
        "PC-DEV-001",
        "PC-DEV-002",
        "PC-MARKETING-001",
        "PC-RH-001",
        "LAPTOP-SALES-001",
        "LAPTOP-ADMIN-001",
        "MAC-DESIGN-001",
        "PC-SUPPORT-001",
    ],
    "network_devices": [
        "SW-CORE-PROD-01",
        "SW-ACCESS-01",
        "RTR-BORDER-01",
        "FW-PERIMETER-01",
        "LB-WEB-PROD-01",
        "AP-WIFI-FLOOR1-01",
    ],
    "storage_devices": [
        "SAN-PROD-01",
        "NAS-BACKUP-01",
        "TAPE-LIBRARY-01",
        "CLOUD-STORAGE-AWS",
    ],
    "applications": [
        "Constellation CMDB",
        "ERP SAP",
        "CRM Salesforce",
        "Active Directory",
        "JIRA Service Desk",
        "Confluence",
        "GitLab CE",
        "Monitoring Zabbix",
        "Slack",
        "Microsoft Teams",
        "Office 365",
        "Antivirus Kaspersky",
    ],
    "system_software": [
        "Windows Server 2019",
        "Ubuntu 20.04",
        "Red Hat Enterprise Linux",
        "VMware vSphere",
        "Docker Engine",
        "Kubernetes",
        "Apache Web Server",
        "Nginx",
    ],
    "middleware": [
        "Apache Tomcat",
        "JBoss EAP",
        "WebLogic Server",
        "RabbitMQ",
        "Apache Kafka",
    ],
    "databases": [
        "PostgreSQL Production",
        "MySQL Development",
        "MongoDB Analytics",
        "Redis Cache",
        "Neo4j Graph DB",
        "Oracle ERP DB",
        "SQL Server CRM",
        "InfluxDB Metrics",
    ],
    "services": [
        "Service Web HTTP",
        "Service API REST",
        "Service Mail SMTP",
        "Service DNS",
        "Service DHCP",
        "Service VPN",
    ],
    "employees": [
        "Marie Dubois (DSI)",
        "Pierre Martin (DevOps)",
        "Sophie Laurent (Dev Senior)",
        "Jean Durand (Admin Sys)",
        "Camille Bernard (Chef Projet)",
        "Lucas Moreau (Analyste)",
        "Emma Petit (Support)",
        "Hugo Simon (Architecte)",
        "Léa Roux (QA)",
        "Thomas Blanc (Sécurité)",
    ],
    "teams": [
        "Équipe DevOps",
        "Équipe Sécurité",
        "Équipe Infrastructure",
        "Équipe Support N2",
        "Équipe Développement",
    ],
    "contractors": [
        "Consultant ACME Corp",
        "Prestataire SecurIT",
        "Freelance Dev Mobile",
    ],
    "policies": [
        "Politique de Sécurité IT",
        "Politique RGPD",
        "Politique Backup",
        "Charte Utilisateur",
    ],
    "procedures": [
        "Procédure Incident Management",
        "Guide Déploiement",
        "Manuel Utilisateur CMDB",
        "Documentation Architecture",
    ],
    "certifications": [
        "Certification ISO 27001",
        "Certification ITIL v4",
        "Certification AWS",
    ],
    "software_licenses": [
        "Licence Microsoft Office 365",
        "Licence VMware vSphere",
        "Licence Adobe Creative Suite",
        "Licence Atlassian Suite",
        "Licence Windows Server",
        "Licence Oracle Database",
    ],
    "contracts": [
        "Contrat Maintenance Dell",
        "Contrat Support Microsoft",
        "Contrat Cloud AWS",
    ],
}

# Types de relations étendus basés sur l'enum du backend
RELATIONSHIP_TYPES = [
    # Relations techniques (enum RelationshipType du backend)
    "DEPENDS_ON",
    "RUNS_ON",
    "HOSTS",
    "CONNECTS_TO",
    "INSTALLED_ON",
    "USES",
    "PRODUCES",
    "CONSUMES",
    "PROCESSES",
    "STORES",
    # Relations humaines
    "OWNS",
    "RESPONSIBLE_FOR",
    "ACCOUNTABLE_FOR",
    "CONSULTED_FOR",
    "INFORMED_FOR",
    "MEMBER_OF",
    "HAS_ROLE",
    "HAS_SKILL",
    # Relations de gouvernance
    "GOVERNED_BY",
    "SUBJECT_TO",
    "COMPLIES_WITH",
    "PROTECTS",
    "COVERS",
    # Relations business
    "OUTSOURCED_TO",
    "PROVIDED_BY",
    "COVERED_BY",
    "CONTRACTED_WITH",
    # Relations de connaissance
    "DOCUMENTS",
    "KNOWS",
    "REFERENCES",
]


def generate_human_attributes():
    """Génère des attributs spécifiques aux humains"""
    departments = [
        "IT",
        "RH",
        "Finance",
        "Marketing",
        "Operations",
        "Direction",
        "Legal",
        "Support",
    ]
    job_titles = [
        "Ingénieur DevOps",
        "Administrateur Système",
        "Développeur Full Stack",
        "Chef de Projet",
        "Analyste Business",
        "Directeur IT",
        "Architecte Solution",
        "Consultant Sécurité",
        "Support N2",
        "Data Analyst",
    ]
    skills = [
        "Python",
        "Docker",
        "Kubernetes",
        "AWS",
        "Linux",
        "Monitoring",
        "Security",
        "Networking",
        "Database",
        "CI/CD",
        "Terraform",
        "Ansible",
    ]

    return {
        "email": fake.email(),
        "department": random.choice(departments),
        "job_title": random.choice(job_titles),
        "manager": "",
        "skills": random.sample(skills, random.randint(2, 5)),
        "certifications": random.choice(
            [
                [],
                ["CISSP"],
                ["AWS Certified"],
                ["ITIL v4"],
                ["CISSP", "ITIL v4"],
                ["AWS Certified", "Docker Certified"],
            ]
        ),
        "phone": fake.phone_number(),
        "employee_id": f"EMP{random.randint(1000, 9999)}",
    }


def generate_license_attributes():
    """Génère des attributs spécifiques aux licences"""
    vendors = [
        "Microsoft",
        "VMware",
        "Oracle",
        "Adobe",
        "Atlassian",
        "AWS",
        "Google",
        "Cisco",
    ]
    license_types = [
        "Per User",
        "Per Device",
        "Site License",
        "Enterprise",
        "Subscription",
        "Perpetual",
    ]
    support_levels = ["Basic", "Standard", "Premium", "Enterprise", "24/7"]

    seats_total = random.choice([5, 10, 25, 50, 100, 250, 500, 1000])
    seats_used = random.randint(
        1, min(seats_total, seats_total - random.randint(0, seats_total // 4))
    )

    return {
        "license_type": random.choice(license_types),
        "vendor": random.choice(vendors),
        "license_key": f"LIC-{random.randint(10000, 99999)}-{random.randint(100, 999)}",
        "seats_total": seats_total,
        "seats_used": seats_used,
        "cost_per_seat": random.choice([5.0, 15.0, 25.0, 50.0, 100.0, 250.0, 500.0]),
        "renewal_date": (
            datetime.now() + timedelta(days=random.randint(30, 730))
        ).strftime("%Y-%m-%d"),
        "support_level": random.choice(support_levels),
    }


def generate_policy_attributes():
    """Génère des attributs spécifiques aux politiques"""
    policy_types = [
        "security",
        "compliance",
        "operational",
        "business",
        "legal",
        "technical",
    ]
    approval_statuses = ["draft", "pending", "approved", "retired", "under_review"]
    frameworks = ["ISO27001", "RGPD", "ITIL", "COBIT", "NIST", "PCI-DSS", "SOX"]
    departments = [
        "IT",
        "Legal",
        "RH",
        "Finance",
        "Operations",
        "Security",
        "Compliance",
    ]

    return {
        "policy_type": random.choice(policy_types),
        "approval_status": random.choice(approval_statuses),
        "approval_date": fake.date_between(start_date="-2y", end_date="today").strftime(
            "%Y-%m-%d"
        )
        if random.choice([True, False])
        else "",
        "review_date": (
            datetime.now() + timedelta(days=random.randint(90, 730))
        ).strftime("%Y-%m-%d"),
        "owner_department": random.choice(departments),
        "compliance_frameworks": random.sample(frameworks, random.randint(1, 3)),
    }


def create_asset(asset_type, template, name):
    """Crée un asset via l'API"""

    # Attributs de base
    asset_data = {
        "name": name,
        "category": template["category"],
        "ci_type": template["ci_type"],
        "criticality": random.choice(template["criticalities"]),
        "description": f"Asset {asset_type} créé automatiquement - {fake.sentence()}",
    }

    # Attributs pour assets tangibles
    if template["category"] == "tangible":
        asset_data.update(
            {
                "environment": random.choice(template["environments"]),
                "lifecycle_state": random.choice(
                    ["ACTIVE", "PLANNED", "DEPRECATED", "RETIRED"]
                ),
                "monitoring_enabled": random.choice([True, False]),
                "backup_enabled": random.choice([True, False]),
            }
        )

        # Attributs techniques pour certains types
        if asset_type in ["servers", "applications", "workstations", "network_devices"]:
            asset_data.update(
                {
                    "hostname": name.replace(" ", "-").lower(),
                    "ip_address": fake.ipv4(),
                    "fqdn": f"{name.replace(' ', '-').lower()}.{random.choice(['company.com', 'internal.local', 'lab.local'])}",
                    "vendor": random.choice(
                        [
                            "Dell",
                            "HP",
                            "Cisco",
                            "VMware",
                            "RedHat",
                            "Microsoft",
                            "IBM",
                            "Oracle",
                        ]
                    ),
                    "model": f"Model-{random.randint(1000, 9999)}",
                    "location": random.choice(
                        [
                            "Datacenter Paris",
                            "Datacenter Lyon",
                            "Cloud AWS EU-West-1",
                            "Office Headquarters",
                            "Site Remote",
                            "Azure West Europe",
                        ]
                    ),
                }
            )

    # Attributs pour assets intangibles
    else:
        intangible_type = template.get("intangible_type", "other")
        asset_data.update(
            {
                "monitoring_enabled": False,
                "backup_enabled": False,
            }
        )

        # Attributs spécifiques par type intangible
        if intangible_type in ["human", "contractor"]:
            asset_data["human_attributes"] = generate_human_attributes()
        elif intangible_type == "license":
            asset_data["license_attributes"] = generate_license_attributes()
        elif intangible_type in [
            "governance",
            "documentation",
            "certification",
            "contract",
        ]:
            asset_data["policy_attributes"] = generate_policy_attributes()

        # Initialiser tous les attributs possibles
        asset_data.update(
            {
                "human_attributes": asset_data.get("human_attributes", {}),
                "license_attributes": asset_data.get("license_attributes", {}),
                "policy_attributes": asset_data.get("policy_attributes", {}),
            }
        )

    try:
        response = requests.post(f"{BASE_URL}/cis", json=asset_data)
        if response.status_code == 201:
            asset_id = response.json().get("id")
            print(f"✅ Créé: {name} ({asset_type}) - ID: {asset_id}")
            return asset_id
        else:
            print(f"❌ Erreur création {name}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception création {name}: {e}")
        return None


def create_relationship(source_id, target_id, relationship_type):
    """Crée une relation entre deux assets"""
    relationship_data = {
        "from_ci_id": source_id,
        "to_ci_id": target_id,
        "relationship_type": relationship_type,
        "description": f"Relation {relationship_type} créée automatiquement",
    }

    try:
        response = requests.post(f"{BASE_URL}/relationships", json=relationship_data)
        if response.status_code == 201:
            print(f"🔗 Relation créée: {source_id} -> {target_id} ({relationship_type})")
            return True
        else:
            print(f"❌ Erreur relation: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception relation: {e}")
        return False


def create_smart_relationships(created_assets):
    """Crée des relations intelligentes entre les assets"""
    print(f"\n🔗 Création de {TOTAL_RELATIONS} relations intelligentes...")

    # Grouper les assets par type pour créer des relations logiques
    assets_by_type = {}
    for asset_id, asset_type in created_assets:
        if asset_type not in assets_by_type:
            assets_by_type[asset_type] = []
        assets_by_type[asset_type].append(asset_id)

    relations_created = 0

    # Relations logiques prédéfinies
    logical_relations = [
        # Infrastructure
        ("applications", "servers", "RUNS_ON"),
        ("applications", "databases", "USES"),
        ("servers", "network_devices", "CONNECTS_TO"),
        ("databases", "storage_devices", "USES"),
        ("services", "servers", "RUNS_ON"),
        # Logiciels
        ("applications", "system_software", "DEPENDS_ON"),
        ("applications", "middleware", "USES"),
        ("system_software", "servers", "INSTALLED_ON"),
        # Humains et organisation
        ("employees", "teams", "MEMBER_OF"),
        ("employees", "applications", "USES"),
        ("teams", "services", "RESPONSIBLE_FOR"),
        ("contractors", "applications", "USES"),
        # Gouvernance
        ("applications", "policies", "GOVERNED_BY"),
        ("employees", "certifications", "HAS_SKILL"),
        ("software_licenses", "applications", "COVERS"),
        ("contracts", "services", "COVERS"),
        # Documentation
        ("procedures", "services", "DOCUMENTS"),
        ("policies", "teams", "SUBJECT_TO"),
    ]

    # Créer des relations basées sur les règles logiques
    for source_type, target_type, rel_type in logical_relations:
        if source_type in assets_by_type and target_type in assets_by_type:
            source_assets = assets_by_type[source_type]
            target_assets = assets_by_type[target_type]

            # Créer quelques relations de ce type
            num_relations = min(3, len(source_assets), len(target_assets))
            for _ in range(num_relations):
                if relations_created >= TOTAL_RELATIONS:
                    break

                source_id = random.choice(source_assets)
                target_id = random.choice(target_assets)

                if source_id != target_id:
                    if create_relationship(source_id, target_id, rel_type):
                        relations_created += 1
                        time.sleep(0.1)  # Petit délai pour éviter la surcharge

    # Compléter avec des relations aléatoires
    all_assets = [asset_id for asset_id, _ in created_assets]
    while relations_created < TOTAL_RELATIONS and len(all_assets) >= 2:
        source_id = random.choice(all_assets)
        target_id = random.choice(all_assets)

        if source_id != target_id:
            rel_type = random.choice(RELATIONSHIP_TYPES)
            if create_relationship(source_id, target_id, rel_type):
                relations_created += 1
                time.sleep(0.1)

            if relations_created >= TOTAL_RELATIONS:
                break

    print(f"🎉 {relations_created} relations créées avec succès!")


def main():
    """Fonction principale"""
    print("🚀 Création complète de données pour Constellation CMDB")
    print(f"📊 Génération de {TOTAL_ASSETS} assets et {TOTAL_RELATIONS} relations...")

    created_assets = []

    # Créer tous les assets
    for asset_type, template in ASSET_TEMPLATES.items():
        print(f"\n📁 Création des {asset_type} ({template['count']} assets)...")

        names = NAMES_BY_TYPE.get(asset_type, [])

        for i in range(template["count"]):
            if i < len(names):
                name = names[i]
            else:
                # Génération de noms supplémentaires si nécessaire
                if "human" in asset_type or asset_type == "employees":
                    name = fake.name()
                elif "team" in asset_type:
                    name = f"Équipe {fake.company().split()[0]}"
                else:
                    name = f"{asset_type.replace('_', ' ').title()} {i+1:02d}"

            asset_id = create_asset(asset_type, template, name)
            if asset_id:
                created_assets.append((asset_id, asset_type))
                time.sleep(0.05)  # Petit délai pour éviter la surcharge

    print(f"\n🎉 Assets créés: {len(created_assets)}")

    # Créer les relations
    if len(created_assets) >= 2:
        create_smart_relationships(created_assets)

    print(f"\n🏆 TERMINÉ!")
    print(f"📈 {len(created_assets)} assets créés")
    print(f"🔗 Jusqu'à {TOTAL_RELATIONS} relations créées")
    print(f"📊 Types d'assets: {len(ASSET_TEMPLATES)}")
    print(f"🔄 Types de relations: {len(RELATIONSHIP_TYPES)}")
    print("\n✨ Votre CMDB est maintenant rempli avec:")
    print("  - Infrastructure complète (serveurs, réseau, stockage)")
    print("  - Applications et logiciels")
    print("  - Équipes et employés")
    print("  - Politiques et documentation")
    print("  - Licences et contrats")
    print("  - Relations intelligentes entre tous les éléments")


if __name__ == "__main__":
    main()
