<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="bg-white shadow">
      <div class="px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">Impact Analysis</h1>
              <p class="mt-2 text-gray-600">Analyze the impact of changes and failures on your infrastructure</p>
            </div>
            <div class="flex items-center space-x-4">
              <!-- Analysis Type Tabs -->
              <div class="flex bg-gray-100 rounded-lg p-1">
                <button
                  @click="activeTab = 'impact'"
                  :class="activeTab === 'impact' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-600'"
                  class="px-4 py-2 text-sm font-medium rounded-md transition-colors"
                >
                  Impact Analysis
                </button>
                <button
                  @click="activeTab = 'dependencies'"
                  :class="activeTab === 'dependencies' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-600'"
                  class="px-4 py-2 text-sm font-medium rounded-md transition-colors"
                >
                  Dependencies
                </button>
                <button
                  @click="activeTab = 'busfactor'"
                  :class="activeTab === 'busfactor' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-600'"
                  class="px-4 py-2 text-sm font-medium rounded-md transition-colors"
                >
                  Bus Factor
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Help Section -->
    <BaseCard shadow="sm" class="bg-blue-50 border-blue-200">
      <div class="flex items-start space-x-3">
        <InformationCircleIcon class="h-6 w-6 text-blue-600 mt-1 flex-shrink-0" />
        <div class="flex-1">
          <h3 class="text-sm font-medium text-blue-900 mb-2">Understanding Impact Analysis</h3>
          
          <!-- Tab-specific explanations -->
          <div v-if="activeTab === 'impact'" class="text-sm text-blue-800 space-y-2">
            <p><strong>Impact Analysis</strong> shows what other CIs would be affected if the selected CI fails or goes down.</p>
            <p>Example: If a database server fails, which applications and services would stop working?</p>
          </div>
          
          <div v-else-if="activeTab === 'dependencies'" class="text-sm text-blue-800 space-y-2">
            <p><strong>Dependency Analysis</strong> shows what other CIs the selected CI depends on to function properly.</p>
            <p>Example: What servers, databases, and services does this application need to run?</p>
          </div>
          
          <div v-else-if="activeTab === 'busfactor'" class="text-sm text-blue-800 space-y-2">
            <p><strong>Bus Factor Analysis</strong> identifies CIs with the highest risk of causing widespread outages.</p>
            <p><strong>Risk Score</strong> = Dependencies × Criticality Multiplier (Critical: 3, High: 2, Medium: 1.5, Low: 1)</p>
            <p>A CI can have high criticality but low risk score if it has few dependencies, and vice versa.</p>
          </div>
          
          <div class="mt-3 pt-2 border-t border-blue-200">
            <p class="text-xs text-blue-700">
              💡 <strong>Tip:</strong> Use max depth to control how far the analysis goes through CI relationships.
            </p>
          </div>
        </div>
      </div>
    </BaseCard>

    <!-- CI Selection -->
    <div v-if="activeTab !== 'busfactor'">
      <CISelector
        v-model="selectedCI"
        :cis="allCIs"
        :is-loading="loadingCIs"
        @search="handleCISearch"
      />
    </div>

    <!-- Analysis Controls -->
    <div v-if="selectedCI && activeTab !== 'busfactor'" class="flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <!-- Max Depth Control -->
        <div class="flex items-center space-x-2">
          <label class="text-sm font-medium text-gray-700">Max Depth:</label>
          <select 
            v-model="maxDepth"
            class="px-3 py-1 border border-gray-300 rounded-md text-sm"
          >
            <option value="1">1 hop</option>
            <option value="2">2 hops</option>
            <option value="3">3 hops</option>
            <option value="4">4 hops</option>
            <option value="5">5 hops</option>
          </select>
        </div>
        
        <!-- Analysis Button -->
        <BaseButton
          @click="runAnalysis"
          :disabled="!selectedCI || isAnalyzing"
          variant="primary"
          size="sm"
        >
          <ArrowPathIcon v-if="isAnalyzing" class="h-4 w-4 animate-spin mr-2" />
          <span v-if="activeTab === 'impact'">Analyze Impact</span>
          <span v-else>Analyze Dependencies</span>
        </BaseButton>
      </div>
      
      <!-- Quick Actions -->
      <div class="flex items-center space-x-2">
        <BaseButton
          v-if="hasResults"
          @click="exportResults"
          variant="outline"
          size="sm"
        >
          <DocumentArrowDownIcon class="h-4 w-4 mr-2" />
          Export
        </BaseButton>
        
        <BaseButton
          v-if="hasResults"
          @click="clearAnalysis"
          variant="outline"
          size="sm"
        >
          <XMarkIcon class="h-4 w-4 mr-2" />
          Clear
        </BaseButton>
      </div>
    </div>

    <!-- Analysis Results -->
    <div class="space-y-6">
      <!-- Impact Analysis Tab -->
      <div v-if="activeTab === 'impact'">
        <!-- No CI Selected State -->
        <BaseCard v-if="!selectedCI" shadow="md">
          <div class="text-center py-12">
            <ExclamationTriangleIcon class="mx-auto h-12 w-12 text-gray-400" />
            <h3 class="mt-2 text-lg font-medium text-gray-900">Impact Analysis</h3>
            <p class="mt-2 text-gray-600">Select a Configuration Item above to analyze its impact</p>
            <p class="text-sm text-gray-500 mt-1">
              Discover what other CIs would be affected if the selected CI fails
            </p>
          </div>
        </BaseCard>

        <!-- Impact Results -->
        <template v-else-if="impactAnalysis">
          <ImpactAnalysisResults
            :analysis="impactAnalysis"
            :source-c-i="selectedCI"
            @view-c-i="handleViewCI"
          />
          
          <!-- Network Visualization -->
          <ImpactNetworkVisualization
            :source-c-i="selectedCI"
            :impact-analysis="impactAnalysis"
            :dependency-analysis="dependencyAnalysis || undefined"
            :is-loading="isAnalyzing"
            @node-click="handleNodeClick"
            @refresh="runAnalysis"
          />
        </template>
        
        <!-- Loading State -->
        <BaseCard v-else-if="isAnalyzing" shadow="md">
          <div class="text-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p class="mt-4 text-sm text-gray-600">Analyzing impact for {{ selectedCI?.name }}...</p>
          </div>
        </BaseCard>
      </div>

      <!-- Dependencies Analysis Tab -->
      <div v-else-if="activeTab === 'dependencies'">
        <!-- No CI Selected State -->
        <BaseCard v-if="!selectedCI" shadow="md">
          <div class="text-center py-12">
            <ShieldCheckIcon class="mx-auto h-12 w-12 text-gray-400" />
            <h3 class="mt-2 text-lg font-medium text-gray-900">Dependency Analysis</h3>
            <p class="mt-2 text-gray-600">Select a Configuration Item above to analyze its dependencies</p>
            <p class="text-sm text-gray-500 mt-1">
              Discover what other CIs this CI depends on to function properly
            </p>
          </div>
        </BaseCard>

        <!-- Dependency Results -->
        <template v-else-if="dependencyAnalysis">
          <DependencyAnalysis
            :analysis="dependencyAnalysis"
            @view-c-i="handleViewCI"
          />
          
          <!-- Network Visualization -->
          <ImpactNetworkVisualization
            :source-c-i="selectedCI"
            :dependency-analysis="dependencyAnalysis || undefined"
            :is-loading="isAnalyzing"
            @node-click="handleNodeClick"
            @refresh="runAnalysis"
          />
        </template>
        
        <!-- Loading State -->
        <BaseCard v-else-if="isAnalyzing" shadow="md">
          <div class="text-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p class="mt-4 text-sm text-gray-600">Analyzing dependencies for {{ selectedCI?.name }}...</p>
          </div>
        </BaseCard>
      </div>

      <!-- Bus Factor Analysis Tab -->
      <div v-else-if="activeTab === 'busfactor'">
        <BaseCard shadow="md">
          <template #header>
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-lg font-medium text-gray-900">Bus Factor Analysis</h3>
                <p class="text-sm text-gray-600 mt-1">Identify CIs with the highest risk of causing widespread outages</p>
              </div>
              <BaseButton
                @click="loadBusFactorAnalysis"
                :disabled="loadingBusFactor"
                variant="primary"
                size="sm"
              >
                <ArrowPathIcon v-if="loadingBusFactor" class="h-4 w-4 animate-spin mr-2" />
                Analyze Bus Factor
              </BaseButton>
            </div>
          </template>

          <!-- Bus Factor Results -->
          <div v-if="busFactorAnalysis">
            <!-- Summary Stats -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div class="bg-red-50 border border-red-200 rounded-lg p-4">
                <div class="text-2xl font-bold text-red-900">{{ busFactorAnalysis.high_risk_cis.length }}</div>
                <div class="text-sm text-red-700">High Risk CIs</div>
              </div>
              <div class="bg-orange-50 border border-orange-200 rounded-lg p-4">
                <div class="text-2xl font-bold text-orange-900">{{ busFactorAnalysis.total_analyzed }}</div>
                <div class="text-sm text-orange-700">Total Analyzed</div>
              </div>
              <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div class="text-2xl font-bold text-blue-900">{{ topRiskScore }}</div>
                <div class="text-sm text-blue-700">Highest Risk Score</div>
              </div>
            </div>

            <!-- High Risk CIs Table -->
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      CI Name
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Type
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Criticality
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Dependencies
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Risk Score
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr 
                    v-for="ci in busFactorAnalysis.high_risk_cis" 
                    :key="ci.ci_id"
                    class="hover:bg-gray-50"
                  >
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="font-medium text-gray-900">{{ ci.ci_name }}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {{ ci.ci_type }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="getCriticalityBadgeColor(ci.criticality)" class="px-2 py-1 rounded-full text-xs font-medium">
                        {{ ci.criticality }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {{ ci.dependency_count }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="getRiskScoreBadgeColor(ci.risk_score)" class="px-2 py-1 rounded-full text-xs font-medium">
                        {{ ci.risk_score }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                      <button
                        @click="analyzeCI(ci.ci_id)"
                        class="text-blue-600 hover:text-blue-900"
                      >
                        Analyze Impact
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Loading State -->
          <div v-else-if="loadingBusFactor" class="text-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p class="mt-4 text-sm text-gray-600">Analyzing bus factor across all CIs...</p>
          </div>

          <!-- Empty State -->
          <div v-else class="text-center py-12">
            <ChartBarIcon class="mx-auto h-12 w-12 text-gray-400" />
            <h3 class="mt-2 text-sm font-medium text-gray-900">Bus Factor Analysis</h3>
            <p class="mt-1 text-sm text-gray-500">
              Click "Analyze Bus Factor" to identify CIs with the highest risk
            </p>
          </div>
        </BaseCard>
      </div>
    </div>

    <!-- Error State -->
    <BaseCard v-if="error" shadow="md">
      <div class="text-center py-12">
        <ExclamationCircleIcon class="mx-auto h-12 w-12 text-red-400" />
        <h3 class="mt-2 text-sm font-medium text-gray-900">Analysis Error</h3>
        <p class="mt-1 text-sm text-gray-500">{{ error }}</p>
        <BaseButton
          @click="clearError"
          variant="outline"
          size="sm"
          class="mt-4"
        >
          Dismiss
        </BaseButton>
      </div>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { 
  ExclamationTriangleIcon, 
  ShieldCheckIcon, 
  ArrowPathIcon,
  DocumentArrowDownIcon,
  XMarkIcon,
  ExclamationCircleIcon,
  ChartBarIcon,
  InformationCircleIcon
} from '@heroicons/vue/24/outline'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import CISelector from '@/components/impact/CISelector.vue'
import ImpactAnalysisResults from '@/components/impact/ImpactAnalysisResults.vue'
import DependencyAnalysis from '@/components/impact/DependencyAnalysis.vue'
import ImpactNetworkVisualization from '@/components/impact/ImpactNetworkVisualization.vue'
import { api } from '@/services/api'
import type { CI, ImpactAnalysis, BusFactorAnalysis } from '@/services/api'

interface DependencyAnalysis {
  source_ci: string
  total_dependencies: number
  dependencies: Array<{
    ci_id: string
    ci_name: string
    criticality: string
    distance: number
    relationship_chain: string[]
  }>
  max_depth_analyzed: number
}

// Router
const router = useRouter()

// State
const activeTab = ref<'impact' | 'dependencies' | 'busfactor'>('impact')
const selectedCI = ref<CI | null>(null)
const maxDepth = ref(3)

// Data
const allCIs = ref<CI[]>([])
const impactAnalysis = ref<ImpactAnalysis | null>(null)
const dependencyAnalysis = ref<DependencyAnalysis | null>(null)
const busFactorAnalysis = ref<BusFactorAnalysis | null>(null)

// Loading states
const loadingCIs = ref(false)
const isAnalyzing = ref(false)
const loadingBusFactor = ref(false)

// Error state
const error = ref<string | null>(null)

// Computed
const hasResults = computed(() => {
  return activeTab.value === 'impact' ? !!impactAnalysis.value :
         activeTab.value === 'dependencies' ? !!dependencyAnalysis.value :
         !!busFactorAnalysis.value
})

const topRiskScore = computed(() => {
  if (!busFactorAnalysis.value?.high_risk_cis?.length) return 0
  return Math.max(...busFactorAnalysis.value.high_risk_cis.map(ci => ci.risk_score))
})

// Methods
const loadCIs = async () => {
  try {
    loadingCIs.value = true
    const response = await api.getCIs({ limit: 5000 }) // Augmenté pour récupérer tous les CIs
    allCIs.value = response.cis || response.items || response || []
  } catch (err) {
    error.value = 'Failed to load Configuration Items'
    console.error('Error loading CIs:', err)
  } finally {
    loadingCIs.value = false
  }
}

const handleCISearch = async (query: string) => {
  if (query.length >= 2) {
    try {
      const response = await api.getCIs({ search: query, limit: 100 })
      const searchResults = response.cis || response.items || response || []
      
      // Mettre les résultats de recherche en priorité, mais garder les autres CIs à la fin
      if (searchResults.length > 0) {
        const existingCIs = allCIs.value.filter((ci: CI) => 
          !searchResults.some((result: any) => result.id === ci.id)
        )
        allCIs.value = [...searchResults, ...existingCIs]
      }
    } catch (err) {
      console.error('Error searching CIs:', err)
    }
  } else if (query.length === 0) {
    // Si la recherche est vidée, recharger tous les CIs
    loadCIs()
  }
}

const runAnalysis = async () => {
  if (!selectedCI.value) return
  
  try {
    isAnalyzing.value = true
    error.value = null
    
    if (activeTab.value === 'impact') {
      impactAnalysis.value = await api.getImpactAnalysis(selectedCI.value.id, maxDepth.value)
    } else if (activeTab.value === 'dependencies') {
      dependencyAnalysis.value = await api.getDependencyAnalysis(selectedCI.value.id, maxDepth.value)
    }
  } catch (err: any) {
    error.value = `Analysis failed: ${err.response?.data?.detail || err.message}`
    console.error('Analysis error:', err)
  } finally {
    isAnalyzing.value = false
  }
}

const loadBusFactorAnalysis = async () => {
  try {
    loadingBusFactor.value = true
    error.value = null
    busFactorAnalysis.value = await api.getBusFactorAnalysis()
  } catch (err: any) {
    error.value = `Bus factor analysis failed: ${err.response?.data?.detail || err.message}`
    console.error('Bus factor analysis error:', err)
  } finally {
    loadingBusFactor.value = false
  }
}

const analyzeCI = async (ciId: string) => {
  const ci = allCIs.value.find(c => c.id === ciId)
  if (ci) {
    selectedCI.value = ci
    activeTab.value = 'impact'
    await runAnalysis()
  }
}

const handleViewCI = (ciId: string) => {
  router.push({ name: 'asset-detail', params: { id: ciId } })
}

const handleNodeClick = (nodeId: string) => {
  const ci = allCIs.value.find(c => c.id === nodeId)
  if (ci && nodeId !== selectedCI.value?.id) {
    selectedCI.value = ci
    runAnalysis()
  }
}

const clearAnalysis = () => {
  impactAnalysis.value = null
  dependencyAnalysis.value = null
  selectedCI.value = null
}

const clearError = () => {
  error.value = null
}

const exportResults = () => {
  const data = activeTab.value === 'impact' ? impactAnalysis.value :
               activeTab.value === 'dependencies' ? dependencyAnalysis.value :
               busFactorAnalysis.value
  
  if (data) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${activeTab.value}-analysis-${new Date().toISOString().split('T')[0]}.json`
    a.click()
    URL.revokeObjectURL(url)
  }
}

const getCriticalityBadgeColor = (criticality: string) => {
  const colors = {
    'CRITICAL': 'bg-red-100 text-red-800',
    'HIGH': 'bg-orange-100 text-orange-800',
    'MEDIUM': 'bg-yellow-100 text-yellow-800',
    'LOW': 'bg-green-100 text-green-800'
  }
  return colors[criticality as keyof typeof colors] || 'bg-gray-100 text-gray-800'
}

const getRiskScoreBadgeColor = (score: number) => {
  if (score >= 50) return 'bg-red-100 text-red-800'
  if (score >= 25) return 'bg-orange-100 text-orange-800'
  if (score >= 10) return 'bg-yellow-100 text-yellow-800'
  return 'bg-green-100 text-green-800'
}

// Watch for selected CI changes
watch(selectedCI, (newCI) => {
  if (newCI && activeTab.value !== 'busfactor') {
    runAnalysis()
  }
})

// Watch for tab changes to trigger analysis if CI is selected
watch(activeTab, (newTab) => {
  error.value = null
  if (selectedCI.value && newTab !== 'busfactor') {
    runAnalysis()
  } else if (newTab === 'busfactor' && !busFactorAnalysis.value) {
    // Auto-load bus factor analysis when switching to that tab
    loadBusFactorAnalysis()
  }
})

// Watch for depth changes
watch(maxDepth, () => {
  if (selectedCI.value && hasResults.value) {
    runAnalysis()
  }
})

// Lifecycle
onMounted(() => {
  loadCIs()
  // Auto-load bus factor if that tab is active on page load
  if (activeTab.value === 'busfactor') {
    loadBusFactorAnalysis()
  }
})
</script>