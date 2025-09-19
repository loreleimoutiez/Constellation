import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Types for our API responses - matching backend structure
export type AssetCategory = 'tangible' | 'intangible'

export type TangibleAssetType = 
  | 'server' | 'database' | 'application' | 'network' | 'storage' | 'service'

export type IntangibleAssetType = 
  | 'human' | 'team' | 'role'           // Human resources
  | 'policy' | 'procedure' | 'standard' // Governance
  | 'license' | 'contract' | 'sla'      // Legal/contractual
  | 'process' | 'workflow'              // Business processes
  | 'knowledge' | 'documentation'       // Intellectual capital
  | 'virtual_machine' | 'container' | 'software' | 'api' | 'microservice' // Logical assets

export interface HumanAttributes {
  email?: string
  department?: string
  job_title?: string
  manager?: string
  skills?: string[]
  certifications?: string[]
  phone?: string
  employee_id?: string
}

export interface PolicyAttributes {
  policy_type?: 'security' | 'compliance' | 'operational' | 'hr'
  approval_status?: 'draft' | 'approved' | 'under_review' | 'deprecated'
  approval_date?: string
  review_date?: string
  owner_department?: string
  compliance_frameworks?: string[]
}

export interface LicenseAttributes {
  license_type?: string
  vendor?: string
  license_key?: string
  seats_total?: number
  seats_used?: number
  cost_per_seat?: number
  renewal_date?: string
  support_level?: string
}

export interface CI {
  id: string
  name: string
  description?: string
  ci_type: string
  // New fields for intangible assets
  category?: AssetCategory
  intangible_type?: IntangibleAssetType
  // Specialized attributes based on type
  human_attributes?: HumanAttributes
  policy_attributes?: PolicyAttributes
  license_attributes?: LicenseAttributes
  // Original fields
  criticality: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW'
  environment?: 'PROD' | 'STAGING' | 'DEV' | 'TEST'
  lifecycle_state?: 'ACTIVE' | 'INACTIVE' | 'PLANNED' | 'DECOMMISSIONED'
  created_at: string
  updated_at: string
  hostname?: string
  ip_address?: string
  fqdn?: string
  vendor?: string
  model?: string
  location?: string
  monitoring_enabled?: boolean
  backup_enabled?: boolean
  // ... other CI properties from backend
}

export type RelationType = 
  // Technical relations (tangible)
  | 'depends_on' | 'connects_to' | 'hosts' | 'uses' | 'communicates_with'
  // Human relations (intangible)  
  | 'assigned_to' | 'managed_by' | 'owned_by' | 'responsible_for'
  // Governance relations
  | 'governed_by' | 'complies_with' | 'approved_by' | 'reviewed_by'
  // Business relations
  | 'licensed_under' | 'requires_skill' | 'supports_process'

export interface Relationship {
  id: string
  type: RelationType
  direction: 'incoming' | 'outgoing'
  related_ci: {
    id: string
    name: string
    category?: AssetCategory
    ci_type: string
  }
  description?: string
  strength?: 'strong' | 'medium' | 'weak'
  created_at?: string
}

export interface ImpactAnalysis {
  source_ci: string
  total_impacted: number
  impacted_cis: Array<{
    ci_id: string
    ci_name: string
    criticality: string
    distance: number
    relationship_chain: string[]
  }>
  criticality_breakdown: {
    CRITICAL: number
    HIGH: number
    MEDIUM: number
    LOW: number
  }
  risk_score: number
  max_depth_analyzed: number
}

export interface BusFactorAnalysis {
  high_risk_cis: Array<{
    ci_id: string
    ci_name: string
    ci_type: string
    criticality: string
    dependency_count: number
    risk_score: number
  }>
  total_analyzed: number
  analysis_date: string
}

// API service class
class ConstellationAPI {
  // CI Management
  async getCIs(params?: { search?: string; limit?: number; offset?: number }) {
    const response = await apiClient.get('/api/v1/cis/', { params })
    return response.data
  }

  async getCI(id: string): Promise<CI> {
    const response = await apiClient.get(`/api/v1/cis/${id}`)
    return response.data
  }

  async createCI(ciData: Partial<CI>): Promise<CI> {
    const response = await apiClient.post('/api/v1/cis/', ciData)
    return response.data
  }

  async createCIWithRelationships(ciData: Partial<CI> & { 
    relationships?: Array<{
      target_ci_id: string
      relationship_type: string
      description?: string
    }> 
  }): Promise<{
    ci: CI
    created_relationships: Array<{
      target_ci_id: string
      relationship_type: string
      description?: string
    }>
    failed_relationships: Array<{
      target_ci_id: string
      relationship_type: string
      error: string
    }>
    success: boolean
  }> {
    const response = await apiClient.post('/api/v1/cis/with-relationships', ciData)
    return response.data
  }

  async updateCI(id: string, ciData: Partial<CI>): Promise<CI> {
    const response = await apiClient.put(`/api/v1/cis/${id}`, ciData)
    return response.data
  }

  async deleteCI(id: string): Promise<void> {
    await apiClient.delete(`/api/v1/cis/${id}`)
  }

  // Relationship Management
  async getRelationships(ciId: string, direction: 'incoming' | 'outgoing' | 'both' = 'both'): Promise<Relationship[]> {
    const response = await apiClient.get(`/api/v1/cis/${ciId}/relationships`, {
      params: { direction }
    })
    return response.data
  }

  async getAllRelationships(limit: number = 100, offset: number = 0): Promise<Relationship[]> {
    const response = await apiClient.get('/api/v1/relationships', {
      params: { limit, offset }
    })
    return response.data
  }

  async createRelationship(relationshipData: {
    from_ci_id: string
    to_ci_id: string
    relationship_type: string
    description?: string
  }) {
    const response = await apiClient.post('/api/v1/relationships', relationshipData)
    return response.data
  }

  async deleteRelationship(relationshipId: string): Promise<void> {
    await apiClient.delete(`/api/v1/relationships/${relationshipId}`)
  }

  // Impact Analysis
  async getImpactAnalysis(ciId: string, maxDepth: number = 3): Promise<ImpactAnalysis> {
    const response = await apiClient.get(`/api/v1/impact/${ciId}`, {
      params: { max_depth: maxDepth }
    })
    return response.data
  }

  async getDependencyAnalysis(ciId: string, maxDepth: number = 3) {
    const response = await apiClient.get(`/api/v1/dependencies/${ciId}`, {
      params: { max_depth: maxDepth }
    })
    return response.data
  }

  async getBusFactorAnalysis(): Promise<BusFactorAnalysis> {
    const response = await apiClient.get('/api/v1/busfactor')
    return response.data
  }

  // Graph Statistics
  async getGraphStats() {
    const response = await apiClient.get('/api/v1/graph/stats')
    return response.data
  }

  // Health Check
  async healthCheck() {
    const response = await apiClient.get('/health')
    return response.data
  }
}

export const api = new ConstellationAPI()
export default api