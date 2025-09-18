import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCMDBStore } from '@/stores/cmdb'

describe('Dashboard Data Debug', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should debug dashboard data loading', async () => {
    const store = useCMDBStore()
    
    console.log('🔍 Initial store state:')
    console.log('  CIs count:', store.cisCount)
    console.log('  CIs array:', store.cis)
    console.log('  Loading:', store.loading)
    console.log('  Error:', store.error)
    
    console.log('\n📡 Fetching CIs...')
    const response = await store.fetchCIs({ limit: 10 })
    
    console.log('\n📊 After fetch:')
    console.log('  API Response:', response)
    console.log('  Store CIs count:', store.cisCount)
    console.log('  Store CIs array length:', store.cis.length)
    console.log('  First CI:', store.cis[0])
    console.log('  Critical CIs:', store.criticalCIs.length)
    console.log('  High CIs:', store.highCIs.length)
    console.log('  Loading:', store.loading)
    console.log('  Error:', store.error)
    
    // Verify the data structure
    expect(store.cis.length).toBeGreaterThan(0)
    expect(store.cisCount).toBeGreaterThan(0)
    
    if (store.cis.length > 0) {
      const firstCI = store.cis[0]
      console.log('\n🔬 First CI structure:')
      console.log('  ID:', firstCI.id)
      console.log('  Name:', firstCI.name)
      console.log('  Type:', firstCI.ci_type)
      console.log('  Criticality:', firstCI.criticality)
      console.log('  Environment:', firstCI.environment)
      console.log('  Lifecycle State:', firstCI.lifecycle_state)
    }
  })
})