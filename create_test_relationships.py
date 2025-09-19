#!/usr/bin/env python3
"""
Script pour créer des relations de test entre les assets existants
"""

import requests
import random
import json

# Configuration API
API_BASE_URL = "http://localhost:8000/api/v1"

def get_all_assets():
    """Récupère tous les assets depuis l'API"""
    try:
        print("🔍 Récupération des assets...")
        response = requests.get(f"{API_BASE_URL}/cis/")
        
        if response.status_code == 200:
            data = response.json()
            assets = data.get('cis', [])
            print(f"✅ {len(assets)} assets trouvés")
            return assets
        else:
            print(f"❌ Erreur API: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return []

def create_relationship(source_id, target_id, relationship_type, description=""):
    """Crée une relation entre deux assets"""
    try:
        data = {
            "from_ci_id": source_id,
            "to_ci_id": target_id,
            "relationship_type": relationship_type,
            "description": description
        }
        
        response = requests.post(f"{API_BASE_URL}/relationships", json=data)
        
        if response.status_code == 201:
            return True
        else:
            print(f"❌ Erreur création relation: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur API: {e}")
        return False

def main():
    """Fonction principale pour créer les relations de test"""
    print("🚀 Démarrage de la création des relations de test")
    
    # Récupération des assets
    all_assets = get_all_assets()
    if not all_assets:
        print("❌ Aucun asset trouvé, arrêt du script")
        return
    
    # Classification des assets par type
    servers = [asset for asset in all_assets if asset.get("ci_type") == "SERVER"]
    applications = [asset for asset in all_assets if asset.get("ci_type") == "APPLICATION"]
    databases = [asset for asset in all_assets if asset.get("ci_type") == "DATABASE"]
    services = [asset for asset in all_assets if asset.get("ci_type") == "SERVICE"]
    networks = [asset for asset in all_assets if asset.get("ci_type") == "NETWORK"]
    people = [asset for asset in all_assets if asset.get("ci_type") == "PERSON"]
    
    print(f"\n📊 Répartition des assets:")
    print(f"   - Serveurs: {len(servers)}")
    print(f"   - Applications: {len(applications)}")
    print(f"   - Bases de données: {len(databases)}")
    print(f"   - Services: {len(services)}")
    print(f"   - Réseaux: {len(networks)}")
    print(f"   - Personnes: {len(people)}")
    
    relations_created = 0
    
    # 1. Applications dépendent de serveurs
    print("\n🔗 Relations: Applications → Serveurs")
    for app in applications[:5]:
        if servers:
            server = random.choice(servers)
            if create_relationship(
                app["id"], 
                server["id"], 
                "DEPENDS_ON",
                f"{app['name']} est hébergé sur {server['name']}"
            ):
                print(f"✅ {app['name']} → DEPENDS_ON → {server['name']}")
                relations_created += 1
    
    # 2. Applications utilisent des bases de données
    print("\n💾 Relations: Applications → Databases")
    for app in applications[:4]:
        if databases:
            db = random.choice(databases)
            if create_relationship(
                app["id"],
                db["id"],
                "USES",
                f"{app['name']} utilise {db['name']}"
            ):
                print(f"✅ {app['name']} → USES → {db['name']}")
                relations_created += 1
    
    # 3. Serveurs hébergent des services
    print("\n🏗️ Relations: Serveurs → Services")
    for server in servers[:4]:
        if services:
            service = random.choice(services)
            if create_relationship(
                server["id"],
                service["id"],
                "HOSTS",
                f"{server['name']} héberge {service['name']}"
            ):
                print(f"✅ {server['name']} → HOSTS → {service['name']}")
                relations_created += 1
    
    # 4. Services utilisent le réseau
    print("\n🌐 Relations: Services → Réseaux")
    for service in services[:3]:
        if networks:
            network = random.choice(networks)
            if create_relationship(
                service["id"],
                network["id"],
                "CONNECTS_TO",
                f"{service['name']} utilise {network['name']}"
            ):
                print(f"✅ {service['name']} → CONNECTS_TO → {network['name']}")
                relations_created += 1
    
    # 5. Personnes responsables des serveurs
    print("\n👤 Relations: Personnes → Serveurs")
    for person in people[:3]:
        if servers:
            server = random.choice(servers)
            if create_relationship(
                person["id"],
                server["id"],
                "RESPONSIBLE_FOR",
                f"{person['name']} gère {server['name']}"
            ):
                print(f"✅ {person['name']} → RESPONSIBLE_FOR → {server['name']}")
                relations_created += 1
    
    # 6. Relations entre assets critiques
    print("\n🔄 Relations: Assets critiques")
    critical_assets = servers[:2] + applications[:2]
    for i, asset1 in enumerate(critical_assets[:-1]):
        asset2 = critical_assets[i + 1]
        if create_relationship(
            asset1["id"],
            asset2["id"],
            "RELATED_TO",
            f"Relation entre {asset1['name']} et {asset2['name']}"
        ):
            print(f"✅ {asset1['name']} → RELATED_TO → {asset2['name']}")
            relations_created += 1
    
    print(f"\n🎉 Création terminée: {relations_created} relations créées avec succès!")

if __name__ == "__main__":
    main()