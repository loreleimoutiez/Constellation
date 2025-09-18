import type { CI, AssetCategory, IntangibleAssetType } from '@/services/api'

// Helper functions for asset display and behavior

export function getAssetCategory(ci: CI): AssetCategory {
  return ci.category || 'tangible'
}

export function isIntangibleAsset(ci: CI): boolean {
  return getAssetCategory(ci) === 'intangible'
}

export function getAssetColor(ci: CI): string {
  const category = getAssetCategory(ci)
  
  if (category === 'intangible') {
    const intangibleColors = {
      // Human resources
      'human': '#8B5CF6',      // Purple
      'team': '#6366F1',       // Indigo  
      'role': '#7C3AED',       // Violet
      
      // Governance
      'policy': '#DC2626',     // Red
      'procedure': '#EA580C',  // Orange
      'standard': '#D97706',   // Amber
      
      // Legal/contractual
      'license': '#059669',    // Emerald
      'contract': '#0D9488',   // Teal
      'sla': '#0891B2',        // Cyan
      
      // Business processes
      'process': '#1D4ED8',    // Blue
      'workflow': '#2563EB',   // Blue
      
      // Knowledge
      'knowledge': '#7C2D12',  // Brown
      'documentation': '#92400E', // Yellow
      
      // Logical assets (ex-logical category)
      'virtual_machine': '#3B82F6', // Blue
      'container': '#06B6D4',       // Cyan
      'software': '#8B5CF6',        // Purple
      'api': '#10B981',             // Green
      'microservice': '#F59E0B'     // Orange
    }
    
    return intangibleColors[ci.intangible_type as IntangibleAssetType] || '#6B7280'
  }
  
  // Tangible asset colors (existing)
  const tangibleColors = {
    'server': '#3B82F6',
    'database': '#10B981', 
    'application': '#8B5CF6',
    'network': '#F59E0B',
    'storage': '#EF4444',
    'service': '#06B6D4'
  }
  
  return tangibleColors[ci.ci_type] || '#6B7280'
}

export function getAssetIcon(ci: CI): string {
  const category = getAssetCategory(ci)
  
  if (category === 'intangible') {
    const intangibleIcons = {
      // Human resources - using heroicons paths
      'human': 'M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z',
      'team': 'M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z',
      'role': 'M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z',
      
      // Governance
      'policy': 'M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 0 0 2.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 0 0-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25ZM6.75 12h.008v.008H6.75V12Zm0 3h.008v.008H6.75V15Zm0 3h.008v.008H6.75V18Z',
      'procedure': 'M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z',
      'standard': 'M11.35 3.836c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m8.9-4.414c.376.023.75.05 1.124.08 1.131.094 1.976 1.057 1.976 2.192V16.5A2.25 2.25 0 0 1 18 18.75h-2.25m-7.5-10.5H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V18.75m-7.5-10.5h6.375c.621 0 1.125.504 1.125 1.125v9.375m-8.25-3 1.5 1.5 3-3.75',
      
      // Legal/contractual  
      'license': 'M15 9h3.75M15 12h3.75M15 15h3.75M4.5 19.5h15a2.25 2.25 0 0 0 2.25-2.25V6.75A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25v10.5A2.25 2.25 0 0 0 4.5 19.5ZM12 9a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Zm-3 8.25a2.25 2.25 0 0 0-2.25-2.25H5.25A2.25 2.25 0 0 0 3 17.25v.75a.75.75 0 0 0 .75.75h4.5a.75.75 0 0 0 .75-.75v-.75Z',
      'contract': 'M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z',
      'sla': 'M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 0 0 2.25-2.25V6.75A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25v10.5A2.25 2.25 0 0 0 4.5 19.5Z',
      
      // Business processes
      'process': 'M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a6.759 6.759 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z',
      'workflow': 'M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0-1 3m1-3h-9.5m0 0 1 3',
      
      // Knowledge
      'knowledge': 'M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25',
      'documentation': 'M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z',
      
      // Logical assets
      'virtual_machine': 'M21.75 17.25v-6a2.25 2.25 0 0 0-2.25-2.25H13.5V7.125c0-1.036-.84-1.875-1.875-1.875h-3.375c-1.036 0-1.875.84-1.875 1.875v1.5c0 1.036.84 1.875 1.875 1.875H9v6.75a2.25 2.25 0 0 0 2.25 2.25h6A2.25 2.25 0 0 0 19.5 19.5Z',
      'container': 'M20.25 7.5l-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z',
      'software': 'M6.75 7.5l3 2.25-3 2.25m4.5 0h3m-9 8.25h13.5A2.25 2.25 0 0 0 21 18V6a2.25 2.25 0 0 0-2.25-2.25H5.25A2.25 2.25 0 0 0 3 6v12a2.25 2.25 0 0 0 2.25 2.25Z',
      'api': 'M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 12H3m18 0h-1.5m-16.5 3.75H3m18 0h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 0 0 2.25-2.25V6.75a2.25 2.25 0 0 0-2.25-2.25H6.75A2.25 2.25 0 0 0 4.5 6.75v10.5a2.25 2.25 0 0 0 2.25 2.25Zm.75-12h9v9h-9v-9Z',
      'microservice': 'M2.25 15a4.5 4.5 0 0 0 4.5 4.5H18a3.75 3.75 0 0 0 1.332-7.257 3 3 0 0 0-3.758-3.848 5.25 5.25 0 0 0-10.233 2.33A4.502 4.502 0 0 0 2.25 15Z'
    }
    
    return intangibleIcons[ci.intangible_type as IntangibleAssetType] || 'M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75'
  }
  
  // Default tangible asset icon (server/computer)
  return 'M21.75 17.25v-6a2.25 2.25 0 0 0-2.25-2.25H13.5V7.125c0-1.036-.84-1.875-1.875-1.875h-3.375c-1.036 0-1.875.84-1.875 1.875v1.5c0 1.036.84 1.875 1.875 1.875H9v6.75a2.25 2.25 0 0 0 2.25 2.25h6A2.25 2.25 0 0 0 19.5 19.5Z'
}

export function getAssetDisplayName(ci: CI): string {
  if (isIntangibleAsset(ci) && ci.intangible_type) {
    const displayNames = {
      'human': 'Person',
      'team': 'Team', 
      'role': 'Role',
      'policy': 'Policy',
      'procedure': 'Procedure',
      'standard': 'Standard',
      'license': 'License',
      'contract': 'Contract',
      'sla': 'SLA',
      'process': 'Process',
      'workflow': 'Workflow',
      'knowledge': 'Knowledge',
      'documentation': 'Documentation',
      'virtual_machine': 'Virtual Machine',
      'container': 'Container',
      'software': 'Software',
      'api': 'API',
      'microservice': 'Microservice'
    }
    
    return displayNames[ci.intangible_type] || ci.ci_type
  }
  
  return ci.ci_type
}

export function getValidEnvironments(ci: CI): string[] {
  if (isIntangibleAsset(ci)) {
    // Most intangible assets don't need traditional environments
    return ['PROD', 'GLOBAL', 'CORPORATE']
  }
  
  return ['PROD', 'STAGING', 'DEV', 'TEST']
}

export function getValidCriticalities(ci: CI): string[] {
  if (isIntangibleAsset(ci)) {
    if (ci.intangible_type === 'human' || ci.intangible_type === 'team') {
      return ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    }
    if (ci.intangible_type === 'policy' || ci.intangible_type === 'license') {
      return ['CRITICAL', 'HIGH', 'MEDIUM']
    }
  }
  
  return ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
}