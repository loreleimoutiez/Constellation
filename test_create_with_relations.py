#!/usr/bin/env python3
"""
Test script for creating CI with relationships endpoint
"""

import requests
import json

def test_create_ci_with_relationships():
    # API endpoint
    url = "http://localhost:8000/api/v1/cis/with-relationships"
    
    # Existing CI IDs from the database (using the ones we just retrieved)
    existing_ci_id = "5ea64c3e-b762-4714-9719-67c177099210"  # Active Directory
    
    # Test data for creating a new CI with relationships
    test_data = {
        "name": "Web Server Frontend",
        "description": "Frontend web server that depends on Active Directory",
        "category": "tangible",
        "ci_type": "HARDWARE",
        "criticality": "HIGH",
        "environment": "PROD",
        "lifecycle_state": "ACTIVE",
        "hostname": "web-frontend-01",
        "ip_address": "192.168.1.100",
        "fqdn": "web-frontend-01.company.com",
        "vendor": "Dell",
        "model": "PowerEdge R740",
        "location": "Datacenter A",
        "relationships": [
            {
                "target_ci_id": existing_ci_id,
                "relationship_type": "DEPENDS_ON",
                "description": "Web server depends on Active Directory for authentication"
            }
        ]
    }
    
    try:
        # Send POST request
        print("Testing CI creation with relationships...")
        print(f"Target CI: {existing_ci_id}")
        print(f"Request data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(url, json=test_data)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Data: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            result = response.json()
            print("\n✅ CI created successfully!")
            print(f"New CI ID: {result['ci']['id']}")
            print(f"Created Relationships: {len(result['created_relationships'])}")
            print(f"Failed Relationships: {len(result['failed_relationships'])}")
            
            if result['failed_relationships']:
                print("\n⚠️ Some relationships failed:")
                for failed in result['failed_relationships']:
                    print(f"  - {failed}")
        else:
            print("\n❌ Failed to create CI")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_create_ci_with_relationships()