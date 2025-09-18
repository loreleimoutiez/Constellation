<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="border-b border-gray-200 pb-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p class="text-gray-600 mt-1">Monitor your infrastructure and configuration items</p>
        </div>
        <div class="flex items-center space-x-3">
          <button 
            @click="refreshData" 
            :disabled="loading"
            class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <svg 
              :class="['w-4 h-4 mr-2', loading ? 'animate-spin' : '']" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refresh
          </button>
          <router-link 
            to="/assets/new" 
            class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Add Asset
          </router-link>
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
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- Total Assets -->
        <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500 mb-1">Total Assets</p>
              <p class="text-3xl font-bold text-gray-900">{{ cisCount }}</p>
              <p class="text-sm text-green-600 mt-1">
                <span class="font-medium">{{ activeAssets }}</span> active
              </p>
            </div>
            <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h6a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h6a2 2 0 002-2v-4a2 2 0 00-2-2m8-8a2 2 0 012 2v4a2 2 0 01-2 2M19 12a2 2 0 012 2v4a2 2 0 01-2 2h-6a2 2 0 01-2-2v-4a2 2 0 012-2" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Critical Assets -->
        <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500 mb-1">Critical Assets</p>
              <p class="text-3xl font-bold text-gray-900">{{ criticalCIs.length }}</p>
              <p class="text-sm text-red-600 mt-1">
                <span class="font-medium">{{ getCriticalPercentage() }}%</span> of total
              </p>
            </div>
            <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- High Priority -->
        <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500 mb-1">High Priority</p>
              <p class="text-3xl font-bold text-gray-900">{{ highCIs.length }}</p>
              <p class="text-sm text-orange-600 mt-1">
                <span class="font-medium">{{ getHighPercentage() }}%</span> of total
              </p>
            </div>
            <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Relationships -->
        <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500 mb-1">Relationships</p>
              <p class="text-3xl font-bold text-gray-900">{{ relationshipCount }}</p>
              <p class="text-sm text-blue-600 mt-1">
                <span class="font-medium">{{ averageConnections }}</span> avg/asset
              </p>
            </div>
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Recent Assets -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg border border-gray-200 shadow-sm">
            <div class="px-6 py-4 border-b border-gray-200">
              <div class="flex items-center justify-between">
                <h3 class="text-lg font-semibold text-gray-900">Recent Assets</h3>
                <router-link 
                  to="/assets" 
                  class="text-sm text-primary-600 hover:text-primary-700 font-medium"
                >
                  View all →
                </router-link>
              </div>
            </div>

            <div class="p-6">
              <div v-if="recentAssets.length === 0" class="text-center py-8">
                <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h6a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h6a2 2 0 002-2v-4a2 2 0 00-2-2m8-8a2 2 0 012 2v4a2 2 0 01-2 2M19 12a2 2 0 012 2v4a2 2 0 01-2 2h-6a2 2 0 01-2-2v-4a2 2 0 012-2" />
                </svg>
                <h3 class="text-lg font-medium text-gray-900 mb-2">No assets found</h3>
                <p class="text-gray-500 mb-6">Get started by creating your first asset.</p>
                <router-link 
                  to="/assets/new" 
                  class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md hover:bg-primary-700"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                  Create Asset
                </router-link>
              </div>

              <div v-else class="space-y-4">
                <div
                  v-for="asset in recentAssets"
                  :key="asset.id"
                  class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
                  @click="$router.push(`/assets/${asset.id}`)"
                >
                  <div class="flex items-center space-x-3">
                    <div
                      :class="[
                        'w-3 h-3 rounded-full',
                        getCriticalityColor(asset.criticality)
                      ]"
                    ></div>
                    <div>
                      <p class="font-medium text-gray-900">{{ asset.name }}</p>
                      <p class="text-sm text-gray-500">{{ asset.ci_type }} • {{ asset.environment }}</p>
                    </div>
                  </div>
                  <div class="text-right">
                    <p class="text-sm text-gray-500">{{ formatDate(asset.created_at) }}</p>
                    <p class="text-xs text-gray-400">{{ asset.lifecycle_state }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- System Overview -->
        <div class="space-y-6">
          <!-- Health Status -->
          <div class="bg-white rounded-lg border border-gray-200 shadow-sm">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-900">System Health</h3>
            </div>
            <div class="p-6 space-y-4">
              <!-- Critical Distribution -->
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-gray-700">Critical Assets</span>
                  <span class="text-sm text-red-600 font-medium">{{ criticalCIs.length }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                    class="bg-red-500 h-2 rounded-full transition-all duration-300"
                    :style="{ width: `${Math.min(getCriticalPercentage(), 100)}%` }"
                  ></div>
                </div>
              </div>

              <!-- High Priority Distribution -->
              <div>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-gray-700">High Priority</span>
                  <span class="text-sm text-orange-600 font-medium">{{ highCIs.length }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                    class="bg-orange-500 h-2 rounded-full transition-all duration-300"
                    :style="{ width: `${Math.min(getHighPercentage(), 100)}%` }"
                  ></div>
                </div>
              </div>

              <!-- Asset Types -->
              <div class="pt-4 border-t border-gray-200">
                <h4 class="text-sm font-medium text-gray-900 mb-3">Asset Types</h4>
                <div class="space-y-2">
                  <div v-for="(count, type) in assetTypeDistribution" :key="type" class="flex justify-between items-center">
                    <span class="text-sm text-gray-600 capitalize">{{ String(type).toLowerCase() }}</span>
                    <span class="text-sm font-medium text-gray-900">{{ count }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="bg-white rounded-lg border border-gray-200 shadow-sm">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-900">Quick Actions</h3>
            </div>
            <div class="p-6 space-y-3">
                            <router-link to="/assets/new" class="block">
                <button class="w-full flex items-center justify-start px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">
                  <PlusIcon class="w-4 h-4 mr-3" />
                  Add New Asset
                </button>
              </router-link>
              <router-link to="/relations" class="block">
                <button class="w-full flex items-center justify-start px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">
                  <svg class="w-4 h-4 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <circle cx="18" cy="5" r="3" />
                    <circle cx="6" cy="12" r="3" />
                    <circle cx="18" cy="19" r="3" />
                    <line x1="8.59" y1="13.51" x2="15.42" y2="17.49" />
                    <line x1="15.41" y1="6.51" x2="8.59" y2="10.49" />
                  </svg>
                  View Relations & Network
                </button>
              </router-link>
              <router-link to="/impact" class="block">
                <button class="w-full flex items-center justify-start px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">
                  <svg class="w-4 h-4 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                  Run Impact Analysis
                </button>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onActivated, computed, nextTick } from 'vue'
import { useCMDBStore } from '@/stores/cmdb'

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
    const apiResponse = await cmdbStore.fetchCIs({ limit: 100 })
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