<template>
  <div class="space-y-8">
    <!-- Page Header -->
    <div class="border-b border-gray-200 pb-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p class="text-gray-600 mt-1">Infrastructure overview and insights</p>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading && cis.length === 0" class="flex justify-center items-center py-16">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
        <p class="text-gray-500">Loading dashboard data...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="mb-6">
      <div class="bg-red-50 border border-red-200 rounded-lg p-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <svg class="h-5 w-5 text-red-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
            <span class="text-red-700">{{ error }}</span>
          </div>
          <button 
            @click="refreshData" 
            class="inline-flex items-center px-3 py-1 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Retry
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else>
      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        <!-- Total Assets -->
        <div @click="navigateToAssets()" 
             class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-1 cursor-pointer">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-blue-100 text-sm font-medium mb-1">Total Assets</p>
              <p class="text-3xl font-bold">{{ cisCount }}</p>
              <p class="text-sm text-blue-100 mt-1">
                <span class="font-medium">{{ activeAssets }}</span> active
              </p>
            </div>
            <div class="w-12 h-12 bg-blue-400 bg-opacity-30 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Critical Assets -->
        <div @click="navigateToCriticalAssets()" 
             class="bg-gradient-to-br from-red-500 to-red-600 rounded-xl p-6 text-white shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-1 cursor-pointer">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-red-100 text-sm font-medium mb-1">Critical Assets</p>
              <p class="text-3xl font-bold">{{ criticalCIs.length }}</p>
              <p class="text-sm text-red-100 mt-1">
                <span class="font-medium">{{ getCriticalPercentage() }}%</span> of total
              </p>
            </div>
            <div class="w-12 h-12 bg-red-400 bg-opacity-30 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- High Priority -->
        <div @click="navigateToHighPriorityAssets()" 
             class="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-6 text-white shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-1 cursor-pointer">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-orange-100 text-sm font-medium mb-1">High Priority</p>
              <p class="text-3xl font-bold">{{ highCIs.length }}</p>
              <p class="text-sm text-orange-100 mt-1">
                <span class="font-medium">{{ getHighPercentage() }}%</span> of total
              </p>
            </div>
            <div class="w-12 h-12 bg-orange-400 bg-opacity-30 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Relationships -->
        <div @click="navigateToRelations()" 
             class="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 text-white shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-1 cursor-pointer">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-green-100 text-sm font-medium mb-1">Relationships</p>
              <p class="text-3xl font-bold">{{ relationshipCount }}</p>
              <p class="text-sm text-green-100 mt-1">
                <span class="font-medium">{{ averageConnections }}</span> avg/asset
              </p>
            </div>
            <div class="w-12 h-12 bg-green-400 bg-opacity-30 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <circle cx="18" cy="5" r="3" />
                <circle cx="6" cy="12" r="3" />
                <circle cx="18" cy="19" r="3" />
                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49" />
                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <!-- Recent Assets -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-xl border border-gray-200 shadow-lg">
            <div class="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-white rounded-t-xl">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                  <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                    <svg class="w-4 h-4 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 class="text-lg font-semibold text-gray-900">Recent Assets</h3>
                </div>
                <router-link 
                  to="/assets" 
                  class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors"
                >
                  View all
                  <svg class="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </router-link>
              </div>
            </div>

            <div class="p-6">
              <div v-if="recentAssets.length === 0" class="text-center py-12">
                <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h6a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h6a2 2 0 002-2v-4a2 2 0 00-2-2m8-8a2 2 0 012 2v4a2 2 0 01-2 2M19 12a2 2 0 012 2v4a2 2 0 01-2 2h-6a2 2 0 01-2-2v-4a2 2 0 012-2" />
                  </svg>
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-2">No assets found</h3>
                <p class="text-gray-500 mb-6">Get started by creating your first asset.</p>
                <router-link 
                  to="/assets/new" 
                  class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Create Asset
                </router-link>
              </div>

              <div v-else class="space-y-3">
                <div
                  v-for="asset in recentAssets"
                  :key="asset.id"
                  class="group flex items-center justify-between p-4 bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl hover:from-blue-50 hover:to-indigo-50 border border-gray-200 hover:border-blue-200 transition-all duration-200 cursor-pointer hover:shadow-md"
                  @click="$router.push(`/assets/${asset.id}`)"
                >
                  <div class="flex items-center space-x-4">
                    <div class="flex-shrink-0">
                      <div
                        :class="[
                          'w-4 h-4 rounded-full border-2 border-white shadow-sm',
                          getCriticalityColor(asset.criticality)
                        ]"
                      ></div>
                    </div>
                    <div class="min-w-0 flex-1">
                      <p class="font-semibold text-gray-900 group-hover:text-blue-900 transition-colors">{{ asset.name }}</p>
                      <div class="flex items-center space-x-2 mt-1">
                        <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          {{ asset.ci_type }}
                        </span>
                        <span v-if="asset.category === 'tangible'" class="text-sm text-gray-500">{{ asset.environment }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="text-right flex-shrink-0">
                    <p class="text-sm font-medium text-gray-600">{{ formatDate(asset.created_at) }}</p>
                    <p v-if="asset.category === 'tangible'" class="text-xs text-gray-400 mt-1">{{ asset.lifecycle_state }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Asset Types Distribution -->
        <div class="bg-white rounded-xl border border-gray-200 shadow-lg">
          <div class="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-white rounded-t-xl">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900">Asset Distribution</h3>
                <p class="text-sm text-gray-500">{{ sortedAssetTypes.length }} types</p>
              </div>
            </div>
          </div>
          
          <div class="p-6">
            <div v-if="sortedAssetTypes.length === 0" class="text-center py-8">
              <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
                </svg>
              </div>
              <p class="text-gray-500">No assets to display</p>
            </div>
            
            <!-- Bar Chart -->
            <div v-else class="space-y-4">
              <div v-for="(item, index) in sortedAssetTypes" :key="item.type" 
                   @click="navigateToAssetsByType(item.type)"
                   class="group cursor-pointer">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-gray-900 capitalize">
                    {{ item.type.replace(/_/g, ' ').toLowerCase() }}
                  </span>
                  <span class="text-sm text-gray-500">{{ item.percentage.toFixed(1) }}%</span>
                </div>
                
                <!-- Progress bar -->
                <div class="relative h-3 bg-gray-200 rounded-full overflow-hidden group-hover:h-4 transition-all duration-200">
                  <div class="absolute inset-0 rounded-full transition-all duration-500 ease-out"
                       :class="index === 0 ? 'bg-gradient-to-r from-blue-500 to-blue-600' : 
                               index === 1 ? 'bg-gradient-to-r from-green-500 to-green-600' : 
                               index === 2 ? 'bg-gradient-to-r from-yellow-500 to-yellow-600' : 
                               index === 3 ? 'bg-gradient-to-r from-purple-500 to-purple-600' : 
                               index === 4 ? 'bg-gradient-to-r from-pink-500 to-pink-600' : 
                               'bg-gradient-to-r from-gray-500 to-gray-600'"
                       :style="{ width: `${Math.max(item.percentage, 5)}%` }">
                  </div>
                  <!-- Animated overlay on hover -->
                  <div class="absolute inset-0 bg-white opacity-0 group-hover:opacity-20 transition-opacity duration-200"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onActivated, computed, nextTick, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCMDBStore } from '@/stores/cmdb'

const router = useRouter()
const cmdbStore = useCMDBStore()

// Use store properties directly to maintain reactivity
const cis = computed(() => cmdbStore.cis)
const cisCount = computed(() => cmdbStore.cisCount)
const criticalCIs = computed(() => cmdbStore.criticalCIs)
const highCIs = computed(() => cmdbStore.highCIs)
const relationships = computed(() => cmdbStore.relationships)
const loading = computed(() => cmdbStore.loading)
const error = computed(() => cmdbStore.error)

// Local computed properties
const relationshipCount = computed(() => relationships.value.length)

const activeAssets = computed(() => {
  return cis.value.filter(ci => ci.lifecycle_state === 'ACTIVE').length
})

const averageConnections = computed(() => {
  if (cisCount.value === 0) return '0'
  return (relationshipCount.value / cisCount.value).toFixed(1)
})

const recentAssets = computed(() => {
  return cis.value
    .slice()
    .sort((a, b) => new Date(b.created_at || '').getTime() - new Date(a.created_at || '').getTime())
    .slice(0, 5)
})

const assetTypeDistribution = computed(() => {
  const distribution: Record<string, number> = {}
  cis.value.forEach(ci => {
    distribution[ci.ci_type] = (distribution[ci.ci_type] || 0) + 1
  })
  return distribution
})

// Sorted asset types for bar chart display
const sortedAssetTypes = computed(() => {
  return Object.entries(assetTypeDistribution.value)
    .sort(([, a], [, b]) => b - a) // Sort by count descending
    .map(([type, count]) => ({
      type,
      count,
      percentage: cisCount.value > 0 ? (count / cisCount.value) * 100 : 0
    }))
})

const getCriticalPercentage = () => {
  if (cisCount.value === 0) return 0
  return Math.round((criticalCIs.value.length / cisCount.value) * 100)
}

const getHighPercentage = () => {
  if (cisCount.value === 0) return 0
  return Math.round((highCIs.value.length / cisCount.value) * 100)
}

const getCriticalityColor = (criticality?: string) => {
  switch (criticality?.toUpperCase()) {
    case 'CRITICAL':
      return 'bg-red-500'
    case 'HIGH':
      return 'bg-orange-500'
    case 'MEDIUM':
      return 'bg-yellow-500'
    case 'LOW':
      return 'bg-green-500'
    default:
      return 'bg-gray-400'
  }
}

// Navigation methods
const navigateToAssets = () => {
  router.push('/assets')
}

const navigateToCriticalAssets = () => {
  router.push({ path: '/assets', query: { criticality: 'CRITICAL' } })
}

const navigateToHighPriorityAssets = () => {
  router.push({ path: '/assets', query: { criticality: 'HIGH' } })
}

const navigateToRelations = () => {
  router.push('/relations')
}

const navigateToAssetsByType = (type: string) => {
  router.push({ path: '/assets', query: { ci_type: type } })
}

const formatDate = (dateString?: string) => {
  if (!dateString) return 'Unknown'
  try {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  } catch {
    return 'Invalid date'
  }
}

const refreshData = async () => {
  try {
    // Load CIs and relationships in parallel
    await Promise.all([
      cmdbStore.fetchCIs({ limit: 100 }),
      cmdbStore.fetchAllRelationships(1000)
    ])
  } catch (err) {
    console.error('Failed to refresh dashboard data:', err)
  }
}

const initializeData = async () => {
  // Check if we already have data
  if (cisCount.value === 0 || cis.value.length === 0) {
    await refreshData()
  }
}

// Load data on mount
onMounted(async () => {
  await nextTick() // Wait for DOM to be ready
  await initializeData()
})

// Also refresh when component becomes active (when navigating back)
onActivated(async () => {
  // Always refresh on activation to ensure fresh data
  await refreshData()
})
</script>