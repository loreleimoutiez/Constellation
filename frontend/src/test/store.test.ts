import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCMDBStore } from '@/stores/cmdb'

describe('CMDB Store Integration', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should fetch and store CIs from backend', async () => {
    const store = useCMDBStore()
    
    expect(store.cis).toEqual([])
    expect(store.loading).toBe(false)
    
    const response = await store.fetchCIs({ limit: 5 })
    
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
    expect(store.cis.length).toBeGreaterThan(0)
    expect(response.total_count).toBeGreaterThan(0)
    
    // Check that a CI has the expected structure
    const firstCI = store.cis[0]
    expect(firstCI).toHaveProperty('id')
    expect(firstCI).toHaveProperty('name')
    expect(firstCI).toHaveProperty('description')
    expect(firstCI).toHaveProperty('ci_type')
    expect(firstCI).toHaveProperty('criticality')
  })

  it('should compute critical and high CIs correctly', async () => {
    const store = useCMDBStore()
    
    await store.fetchCIs()
    
    const criticalCount = store.criticalCIs.length
    const highCount = store.highCIs.length
    
    expect(typeof criticalCount).toBe('number')
    expect(typeof highCount).toBe('number')
    
    // Verify that critical CIs are actually critical
    store.criticalCIs.forEach(ci => {
      expect(ci.criticality).toBe('CRITICAL')
    })
    
    store.highCIs.forEach(ci => {
      expect(ci.criticality).toBe('HIGH')
    })
  })

  it('should fetch graph statistics', async () => {
    const store = useCMDBStore()
    
    const stats = await store.fetchGraphStats()
    
    expect(store.error).toBeNull()
    expect(stats).toBeDefined()
    expect(stats.total_cis).toBeGreaterThan(0)
    expect(stats.total_relationships).toBeGreaterThanOrEqual(0)
  })
})