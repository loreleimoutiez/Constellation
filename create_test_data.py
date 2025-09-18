#!/usr/bin/env python3
"""
Script pour créer des données de test variées pour Constellation CMDB
Génère 50+ assets de différents types pour tester tous les affichages
"""

import requests
import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('fr_FR')

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
TOTAL_ASSETS = 55

# Données de test structurées
ASSET_TEMPLATES = {
    # ASSETS TANGIBLES
    "servers": {
        "category": "tangible",
        "ci_type": "HARDWARE",
        "environments": ["PROD", "DEV", "TEST", "STAGING"],
        "criticalities": ["HIGH", "MEDIUM", "LOW"],
        "count": 12
    },
    "applications": {
        "category": "tangible", 
        "ci_type": "APPLICATION",
        "environments": ["PROD", "DEV", "TEST"],
        "criticalities": ["HIGH", "MEDIUM", "LOW"],
        "count": 8
    },
    "databases": {
        "category": "tangible",
        "ci_type": "DATABASE", 
        "environments": ["PROD", "DEV", "TEST"],
        "criticalities": ["HIGH", "MEDIUM"],
        "count": 6
    },
    "networks": {
        "category": "tangible",
        "ci_type": "NETWORK",
        "environments": ["PROD", "DEV"],
        "criticalities": ["HIGH", "MEDIUM", "LOW"],
        "count": 4
    },
    "services": {
        "category": "tangible",
        "ci_type": "SERVICE",
        "environments": ["PROD", "DEV", "TEST"],
        "criticalities": ["HIGH", "MEDIUM", "LOW"],
        "count": 5
    },
    
    # ASSETS TANGIBLES SUPPLÉMENTAIRES
    "endpoints": {
        "category": "tangible",
        "ci_type": "ENDPOINT",
        "environments": ["PROD", "DEV"],
        "criticalities": ["MEDIUM", "LOW"],
        "count": 4
    },
    "software": {
        "category": "tangible",
        "ci_type": "SOFTWARE",
        "environments": ["PROD", "DEV", "TEST"],
        "criticalities": ["HIGH", "MEDIUM"],
        "count": 3
    },
    
    # ASSETS INTANGIBLES - HUMAINS
    "humans": {
        "category": "intangible",
        "ci_type": "IDENTITY",
        "criticalities": ["HIGH", "MEDIUM", "LOW"],
        "count": 8,
        "intangible_type": "human"
    },
    
    # ASSETS INTANGIBLES - ÉQUIPES  
    "teams": {
        "category": "intangible",
        "ci_type": "IDENTITY", 
        "criticalities": ["HIGH", "MEDIUM"],
        "count": 4,
        "intangible_type": "team"
    },
    
    # ASSETS INTANGIBLES - GOUVERNANCE
    "policies": {
        "category": "intangible",
        "ci_type": "DATASET",
        "criticalities": ["HIGH", "MEDIUM", "LOW"],
        "count": 3,
        "intangible_type": "governance"
    },
    
    # ASSETS INTANGIBLES - DOCUMENTATION
    "documentation": {
        "category": "intangible", 
        "ci_type": "DATASET",
        "criticalities": ["MEDIUM", "LOW"],
        "count": 3,
        "intangible_type": "documentation"
    },
    
    # ASSETS INTANGIBLES - LICENCES
    "licenses": {
        "category": "intangible",
        "ci_type": "GENERIC", 
        "criticalities": ["HIGH", "MEDIUM"],
        "count": 2,
        "intangible_type": "license"
    }
}

# Noms réalistes par type
NAMES_BY_TYPE = {
    "servers": [
        "srv-web-prod-01", "srv-app-dev-02", "srv-db-prod-03", "srv-backup-01",
        "srv-monitoring-01", "srv-file-share-02", "srv-mail-prod-01", "srv-dns-01",
        "srv-proxy-prod-01", "srv-jenkins-dev-01", "srv-gitlab-prod-01", "srv-elk-stack-01"
    ],
    "applications": [
        "Constellation CMDB", "ERP SAP", "CRM Salesforce", "Active Directory", 
        "JIRA Service Desk", "Confluence", "GitLab CE", "Monitoring Zabbix"
    ],
    "databases": [
        "PostgreSQL Production", "MySQL Development", "MongoDB Analytics", 
        "Redis Cache", "Neo4j Graph DB", "Oracle ERP DB"
    ],
    "networks": [
        "LAN Production", "DMZ Network", "VPN Tunnel", "WiFi Corporate"
    ],
    "services": [
        "Service Web", "Service API", "Service Mail", "Service DNS", "Service DHCP"
    ],
    "endpoints": [
        "Poste Développeur 01", "Laptop Marketing 02", "Tablette Vente 03", "PC Bureau RH 01"
    ],
    "software": [
        "Adobe Creative Suite", "Microsoft Visual Studio", "Docker Engine"
    ],
    "humans": [
        "Marie Dubois", "Pierre Martin", "Sophie Laurent", "Jean Durand",
        "Camille Bernard", "Lucas Moreau", "Emma Petit", "Hugo Simon"
    ],
    "teams": [
        "Équipe DevOps", "Équipe Sécurité", "Équipe Infrastructure", "Équipe Support"
    ],
    "policies": [
        "Politique de Sécurité IT", "Procédure de Backup", "Politique RGPD"
    ],
    "documentation": [
        "Guide d'Architecture", "Manuel Utilisateur", "Documentation API"
    ],
    "licenses": [
        "Licence Microsoft Office 365", "Licence VMware vSphere"
    ]
}

def generate_human_attributes():
    """Génère des attributs spécifiques aux humains"""
    departments = ["IT", "RH", "Finance", "Marketing", "Operations", "Direction"]
    job_titles = ["Ingénieur DevOps", "Administrateur Système", "Développeur", "Chef de Projet", "Analyste", "Directeur IT"]
    skills = ["Python", "Docker", "Kubernetes", "AWS", "Linux", "Monitoring", "Security", "Networking"]
    
    return {
        "email": fake.email(),
        "department": random.choice(departments),
        "job_title": random.choice(job_titles),
        "manager": "",
        "skills": random.sample(skills, random.randint(2, 4)),
        "certifications": random.choice([[], ["CISSP"], ["AWS Certified"], ["CISSP", "ITIL v4"]]),
        "phone": fake.phone_number(),
        "employee_id": f"EMP{random.randint(1000, 9999)}"
    }

def generate_license_attributes():
    """Génère des attributs spécifiques aux licences"""
    vendors = ["Microsoft", "VMware", "Oracle", "Adobe", "Atlassian"]
    license_types = ["Per User", "Per Device", "Site License", "Enterprise"]
    support_levels = ["Basic", "Standard", "Premium", "Enterprise"]
    
    seats_total = random.choice([10, 25, 50, 100, 250, 500])
    seats_used = random.randint(1, seats_total)
    
    return {
        "license_type": random.choice(license_types),
        "vendor": random.choice(vendors),
        "license_key": f"LIC-{random.randint(10000, 99999)}-{random.randint(100, 999)}",
        "seats_total": seats_total,
        "seats_used": seats_used,
        "cost_per_seat": random.choice([15.0, 25.0, 50.0, 100.0, 250.0]),
        "renewal_date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
        "support_level": random.choice(support_levels)
    }

def generate_policy_attributes():
    """Génère des attributs spécifiques aux politiques"""
    policy_types = ["security", "compliance", "operational", "business"]
    approval_statuses = ["draft", "pending", "approved", "retired"]
    frameworks = ["ISO27001", "RGPD", "ITIL", "COBIT", "NIST"]
    departments = ["IT", "Legal", "RH", "Finance", "Operations"]
    
    return {
        "policy_type": random.choice(policy_types),
        "approval_status": random.choice(approval_statuses),
        "approval_date": fake.date_between(start_date='-1y', end_date='today').strftime("%Y-%m-%d") if random.choice([True, False]) else "",
        "review_date": (datetime.now() + timedelta(days=random.randint(90, 365))).strftime("%Y-%m-%d"),
        "owner_department": random.choice(departments),
        "compliance_frameworks": random.sample(frameworks, random.randint(1, 3))
    }

def create_asset(asset_type, template, name):
    """Crée un asset via l'API"""
    
    # Attributs de base
    asset_data = {
        "name": name,
        "category": template["category"],
        "ci_type": template["ci_type"],
        "criticality": random.choice(template["criticalities"]),
        "description": f"Asset de test - {asset_type}",
    }
    
    # Attributs pour assets tangibles
    if template["category"] == "tangible":
        asset_data.update({
            "environment": random.choice(template["environments"]),
            "lifecycle_state": random.choice(["ACTIVE", "PLANNED", "DEPRECATED"]),
            "monitoring_enabled": random.choice([True, False]),
            "backup_enabled": random.choice([True, False]),
        })
        
        # Attributs techniques pour certains types
        if asset_type in ["servers", "applications"]:
            asset_data.update({
                "hostname": name.replace(" ", "-").lower(),
                "ip_address": fake.ipv4(),
                "fqdn": f"{name.replace(' ', '-').lower()}.{random.choice(['company.com', 'internal.local'])}",
                "vendor": random.choice(["Dell", "HP", "Cisco", "VMware", "RedHat"]),
                "model": f"Model-{random.randint(1000, 9999)}",
                "location": random.choice(["Datacenter A", "Datacenter B", "Cloud AWS", "Office Paris"])
            })
    
    # Attributs pour assets intangibles
    else:
        intangible_type = template.get("intangible_type", "other")
        asset_data.update({
            "monitoring_enabled": False,
            "backup_enabled": False,
            "custom_attributes": {
                "original_intangible_type": intangible_type,
                "is_intangible_asset": True
            }
        })
        
        # Attributs spécifiques par type intangible
        if intangible_type == "human":
            asset_data["human_attributes"] = generate_human_attributes()
        elif intangible_type == "license":
            asset_data["license_attributes"] = generate_license_attributes()
        elif intangible_type in ["governance", "documentation"]:
            asset_data["policy_attributes"] = generate_policy_attributes()
        
        # Attributs vides pour les autres types
        asset_data.update({
            "human_attributes": asset_data.get("human_attributes", {}),
            "license_attributes": asset_data.get("license_attributes", {}),
            "policy_attributes": asset_data.get("policy_attributes", {})
        })
    
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

def main():
    """Fonction principale"""
    print("🚀 Création de données de test pour Constellation CMDB")
    print(f"📊 Génération de {TOTAL_ASSETS} assets...")
    
    created_assets = []
    
    for asset_type, template in ASSET_TEMPLATES.items():
        print(f"\n📁 Création des {asset_type} ({template['count']} assets)...")
        
        names = NAMES_BY_TYPE.get(asset_type, [])
        
        for i in range(template["count"]):
            if i < len(names):
                name = names[i]
            else:
                # Génération de noms supplémentaires si nécessaire
                if asset_type == "humans":
                    name = fake.name()
                elif asset_type == "teams":
                    name = f"Équipe {fake.company()}"
                else:
                    name = f"{asset_type.title()} {i+1}"
            
            asset_id = create_asset(asset_type, template, name)
            if asset_id:
                created_assets.append(asset_id)
    
    print(f"\n🎉 Terminé! {len(created_assets)} assets créés avec succès")
    print(f"📈 Types créés: {', '.join(ASSET_TEMPLATES.keys())}")
    print("\n🔄 Vous pouvez maintenant tester:")
    print("  - Dashboard avec distribution des types")
    print("  - Vue Assets avec filtres")
    print("  - Fiches détaillées par catégorie")
    print("  - Création de relations entre assets")

if __name__ == "__main__":
    main()