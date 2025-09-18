import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCMDBStore } from '@/stores/cmdb'

describe('Dashboard Fix Validation', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should load CIs correctly and display proper counts', async () => {
    console.log('🎯 Testing Dashboard Data Loading After CORS Fix...')
    
    const store = useCMDBStore()
    
    // Initial state
    console.log('1. Initial state:')
    console.log(`   - CIs count: ${store.cisCount}`)
    console.log(`   - Loading: ${store.loading}`)
    console.log(`   - Error: ${store.error}`)
    
    // Fetch data like the dashboard does
    console.log('\n2. Fetching CIs (limit 100)...')
    const response = await store.fetchCIs({ limit: 100 })
    
    // Verify results
    console.log('\n3. Results after fetch:')
    console.log(`   - API response total: ${response.total_count}`)
    console.log(`   - Store CIs count: ${store.cisCount}`)
    console.log(`   - Critical CIs: ${store.criticalCIs.length}`)
    console.log(`   - High CIs: ${store.highCIs.length}`)
    console.log(`   - Loading: ${store.loading}`)
    console.log(`   - Error: ${store.error}`)
    
    // Expectations
    expect(store.error).toBeNull()
    expect(store.loading).toBe(false)
    expect(store.cisCount).toBeGreaterThan(0)
    expect(response.total_count).toBeGreaterThan(0)
    expect(store.cisCount).toBe(response.cis.length)
    
    // Test computed properties
    const criticalCount = store.criticalCIs.length
    const highCount = store.highCIs.length
    
    console.log('\n4. Computed properties:')
    console.log(`   - Critical assets: ${criticalCount}`)
    console.log(`   - High priority assets: ${highCount}`)
    
    expect(typeof criticalCount).toBe('number')
    expect(typeof highCount).toBe('number')
    
    // Show sample data
    if (store.cis.length > 0) {
      const firstCI = store.cis[0]
      console.log('\n5. Sample CI:')
      console.log(`   - Name: ${firstCI.name}`)
      console.log(`   - Type: ${firstCI.ci_type}`)
      console.log(`   - Criticality: ${firstCI.criticality}`)
      console.log(`   - Environment: ${firstCI.environment}`)
    }
    
    console.log('\n🎉 Dashboard should now display correct data!')
    console.log(`✅ Total Assets: ${store.cisCount}`)
    console.log(`✅ Critical Assets: ${criticalCount}`)
    console.log(`✅ High Priority: ${highCount}`)
  })
})