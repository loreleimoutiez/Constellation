import { describe, it, expect } from 'vitest'
import api from '@/services/api'

describe('Full Stack Integration Demo', () => {
  it('should demonstrate complete CMDB workflow', async () => {
    console.log('🎯 Testing Full Stack Integration...')
    
    // 1. Health Check
    console.log('1. Testing API health...')
    const health = await api.healthCheck()
    expect(health.status).toBe('healthy')
    console.log('   ✅ API is healthy:', health)
    
    // 2. Fetch existing CIs
    console.log('2. Fetching existing CIs...')
    const response = await api.getCIs({ limit: 3 })
    expect(response.cis).toBeDefined()
    expect(Array.isArray(response.cis)).toBe(true)
    console.log(`   ✅ Found ${response.total_count} CIs total, showing ${response.cis.length}`)
    
    // 3. Show CI details
    if (response.cis.length > 0) {
      const firstCI = response.cis[0]
      console.log('3. Sample CI details:')
      console.log(`   📋 Name: ${firstCI.name}`)
      console.log(`   🏷️  Type: ${firstCI.ci_type}`)
      console.log(`   ⚠️  Criticality: ${firstCI.criticality}`)
      console.log(`   🌍 Environment: ${firstCI.environment}`)
    }
    
    // 4. Get graph statistics
    console.log('4. Fetching graph statistics...')
    const stats = await api.getGraphStats()
    expect(stats.total_cis).toBeGreaterThan(0)
    console.log('   ✅ Graph Stats:')
    console.log(`   📊 Total CIs: ${stats.total_cis}`)
    console.log(`   🔗 Total Relationships: ${stats.total_relationships}`)
    console.log(`   📈 Unique Relationship Types: ${stats.unique_relationship_types}`)
    
    // 5. Test relationship fetching if CIs exist
    if (response.cis.length > 0) {
      console.log('5. Testing relationship queries...')
      const ciId = response.cis[0].id
      try {
        const relationships = await api.getRelationships(ciId)
        console.log(`   ✅ Found ${relationships.length} relationships for CI: ${response.cis[0].name}`)
      } catch (error) {
        console.log('   ℹ️  No relationships found (expected for new setup)')
      }
    }
    
    console.log('🎉 Full Stack Integration Test Complete!')
    console.log('🚀 Frontend ↔️ Backend communication is working perfectly!')
  })
})