import { describe, it, expect } from 'vitest'
import api from '@/services/api'
import type { CI } from '@/services/api'

describe('Dashboard Data Verification', () => {
  it('should verify dashboard can load real data from API', async () => {
    console.log('🔍 Testing Dashboard Data Loading...')
    
    // Simulate what the dashboard does on mount
    console.log('1. Fetching CIs with limit 100 (dashboard default)...')
    const response = await api.getCIs({ limit: 100 })
    
    console.log('📊 API Response:')
    console.log('  - Total CIs in DB:', response.total_count)
    console.log('  - CIs returned:', response.cis.length)
    console.log('  - Limit used:', response.limit)
    console.log('  - Offset:', response.offset)
    
    // Verify we have data
    expect(response.total_count).toBeGreaterThan(0)
    expect(response.cis.length).toBeGreaterThan(0)
    
    // Count by criticality (what dashboard displays)
    const critical = response.cis.filter((ci: CI) => ci.criticality === 'CRITICAL')
    const high = response.cis.filter((ci: CI) => ci.criticality === 'HIGH')
    const medium = response.cis.filter((ci: CI) => ci.criticality === 'MEDIUM')
    const low = response.cis.filter((ci: CI) => ci.criticality === 'LOW')
    
    console.log('\n📈 Criticality Breakdown:')
    console.log(`  - Critical: ${critical.length}`)
    console.log(`  - High: ${high.length}`)
    console.log(`  - Medium: ${medium.length}`)
    console.log(`  - Low: ${low.length}`)
    console.log(`  - Total: ${response.cis.length}`)
    
    // Show some CI details
    if (response.cis.length > 0) {
      console.log('\n🏷️  Sample CIs:')
      response.cis.slice(0, 3).forEach((ci: CI, idx: number) => {
        console.log(`  ${idx + 1}. ${ci.name} (${ci.ci_type}, ${ci.criticality})`)
      })
    }
    
    console.log('\n✅ Dashboard should now display:')
    console.log(`   Total Assets: ${response.cis.length}`)
    console.log(`   Critical Assets: ${critical.length}`)
    console.log(`   High Priority: ${high.length}`)
    
    // Test graph stats too
    const stats = await api.getGraphStats()
    console.log(`   Relationships: ${stats.total_relationships}`)
  })
})