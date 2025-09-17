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
export interface CI {
  id: string
  name: string
  description?: string
  ci_type: string
  criticality: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW'
  environment: 'PROD' | 'STAGING' | 'DEV' | 'TEST'
  lifecycle_state: 'ACTIVE' | 'INACTIVE' | 'PLANNED' | 'DECOMMISSIONED'
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

export interface Relationship {
  id: string
  type: string
  direction: 'incoming' | 'outgoing'
  related_ci: {
    id: string
    name: string
  }
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