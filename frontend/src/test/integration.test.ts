import { describe, it, expect, beforeAll } from 'vitest'
import api from '@/services/api'

describe('API Integration Tests', () => {
  beforeAll(async () => {
    // Wait a bit for services to be ready
    await new Promise(resolve => setTimeout(resolve, 2000))
  })

  it('should connect to backend health endpoint', async () => {
    const response = await api.healthCheck()
    expect(response).toBeDefined()
    expect(response.status).toBe('healthy')
    expect(response.database).toBe('connected')
  })

  it('should fetch CIs from backend', async () => {
    const response = await api.getCIs({ limit: 10 })
    expect(response).toBeDefined()
    expect(Array.isArray(response.cis)).toBe(true)
    expect(typeof response.total_count).toBe('number')
    expect(typeof response.limit).toBe('number')
    expect(typeof response.offset).toBe('number')
  })

  it('should fetch graph stats', async () => {
    const stats = await api.getGraphStats()
    expect(stats).toBeDefined()
    expect(typeof stats.total_cis).toBe('number')
    expect(typeof stats.total_relationships).toBe('number')
    expect(typeof stats.unique_relationship_types).toBe('number')
  })
})