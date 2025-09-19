import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { CI, Relationship, ImpactAnalysis, BusFactorAnalysis } from '@/services/api'
import api from '@/services/api'

export const useCMDBStore = defineStore('cmdb', () => {
  // State
  const cis = ref<CI[]>([])
  const selectedCI = ref<CI | null>(null)
  const relationships = ref<Relationship[]>([])
  const impactAnalysis = ref<ImpactAnalysis | null>(null)
  const busFactorAnalysis = ref<BusFactorAnalysis | null>(null)
  const graphStats = ref<any>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const cisCount = computed(() => cis.value.length)
  const criticalCIs = computed(() => 
    cis.value.filter(ci => ci.criticality === 'CRITICAL')
  )
  const highCIs = computed(() => 
    cis.value.filter(ci => ci.criticality === 'HIGH')
  )

  // Actions
  async function fetchCIs(params?: { search?: string; limit?: number; offset?: number }) {
    loading.value = true
    error.value = null
    try {
      const response = await api.getCIs(params)
      cis.value = response.cis || []
      return response
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch CIs'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchCI(id: string) {
    loading.value = true
    error.value = null
    try {
      const ci = await api.getCI(id)
      selectedCI.value = ci
      return ci
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch CI'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createCI(ciData: Partial<CI>) {
    loading.value = true
    error.value = null
    try {
      const newCI = await api.createCI(ciData)
      cis.value.push(newCI)
      return newCI
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create CI'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createCIWithRelationships(ciData: Partial<CI> & { relationships?: Array<{
    target_ci_id: string
    relationship_type: string
    description?: string
  }> }) {
    loading.value = true
    error.value = null
    try {
      const response = await api.createCIWithRelationships(ciData)
      cis.value.push(response.ci)
      return response
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create CI with relationships'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateCI(id: string, ciData: Partial<CI>) {
    loading.value = true
    error.value = null
    try {
      const updatedCI = await api.updateCI(id, ciData)
      const index = cis.value.findIndex(ci => ci.id === id)
      if (index !== -1) {
        cis.value[index] = updatedCI
      }
      if (selectedCI.value?.id === id) {
        selectedCI.value = updatedCI
      }
      return updatedCI
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update CI'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteCI(id: string) {
    loading.value = true
    error.value = null
    try {
      await api.deleteCI(id)
      cis.value = cis.value.filter(ci => ci.id !== id)
      if (selectedCI.value?.id === id) {
        selectedCI.value = null
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete CI'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchRelationships(ciId: string, direction: 'incoming' | 'outgoing' | 'both' = 'both') {
    loading.value = true
    error.value = null
    try {
      const rels = await api.getRelationships(ciId, direction)
      relationships.value = rels
      return rels
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch relationships'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchAllRelationships(limit: number = 1000) {
    loading.value = true
    error.value = null
    try {
      const rels = await api.getAllRelationships(limit, 0)
      relationships.value = rels
      return rels
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch all relationships'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createRelationship(relationshipData: {
    from_ci_id: string
    to_ci_id: string
    relationship_type: string
    description?: string
  }) {
    loading.value = true
    error.value = null
    try {
      const result = await api.createRelationship(relationshipData)
      // Refresh relationships if we're viewing one of the related CIs
      if (selectedCI.value && 
          (selectedCI.value.id === relationshipData.from_ci_id || 
           selectedCI.value.id === relationshipData.to_ci_id)) {
        await fetchRelationships(selectedCI.value.id)
      }
      return result
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create relationship'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteRelationship(id: string) {
    loading.value = true
    error.value = null
    try {
      const result = await api.deleteRelationship(id)
      return result
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete relationship'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchImpactAnalysis(ciId: string, maxDepth: number = 3) {
    loading.value = true
    error.value = null
    try {
      const analysis = await api.getImpactAnalysis(ciId, maxDepth)
      impactAnalysis.value = analysis
      return analysis
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch impact analysis'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchBusFactorAnalysis() {
    loading.value = true
    error.value = null
    try {
      const analysis = await api.getBusFactorAnalysis()
      busFactorAnalysis.value = analysis
      return analysis
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch bus factor analysis'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchGraphStats() {
    loading.value = true
    error.value = null
    try {
      const stats = await api.getGraphStats()
      graphStats.value = stats
      return stats
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch graph stats'
      throw err
    } finally {
      loading.value = false
    }
  }

  function clearError() {
    error.value = null
  }

  function setSelectedCI(ci: CI | null) {
    selectedCI.value = ci
  }

  return {
    // State
    cis,
    selectedCI,
    relationships,
    impactAnalysis,
    busFactorAnalysis,
    graphStats,
    loading,
    error,
    
    // Computed
    cisCount,
    criticalCIs,
    highCIs,
    
    // Actions
    fetchCIs,
    fetchCI,
    createCI,
    createCIWithRelationships,
    updateCI,
    deleteCI,
    fetchRelationships,
    fetchAllRelationships,
    createRelationship,
    deleteRelationship,
    fetchImpactAnalysis,
    fetchBusFactorAnalysis,
    fetchGraphStats,
    clearError,
    setSelectedCI,
  }
})