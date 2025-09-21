<template>
  <div class="space-y-6">
    <!-- Analysis Overview -->
    <BaseCard shadow="md">
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900">Impact Analysis Results</h3>
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-500">Max Depth: {{ analysis.max_depth_analyzed }}</span>
            <div :class="getRiskScoreColor(analysis.risk_score)" class="px-3 py-1 rounded-full text-sm font-medium">
              Risk Score: {{ analysis.risk_score }}
            </div>
          </div>
        </div>
      </template>

      <!-- Source CI Info -->
      <div class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <div class="flex items-center space-x-3">
          <ExclamationTriangleIcon class="h-8 w-8 text-blue-600" />
          <div>
            <h4 class="font-medium text-blue-900">Analyzing Impact of</h4>
            <p class="text-blue-700">{{ sourceCI?.name || analysis.source_ci }}</p>
            <p class="text-sm text-blue-600">{{ sourceCI?.ci_type }} • {{ sourceCI?.criticality }}</p>
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-red-50 border border-red-200 rounded-lg p-4">
          <div class="text-2xl font-bold text-red-900">{{ analysis.total_impacted }}</div>
          <div class="text-sm text-red-700">Total Impacted CIs</div>
        </div>
        
        <div class="bg-orange-50 border border-orange-200 rounded-lg p-4">
          <div class="text-2xl font-bold text-orange-900">{{ analysis.criticality_breakdown.CRITICAL }}</div>
          <div class="text-sm text-orange-700">Critical Impact</div>
        </div>
        
        <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div class="text-2xl font-bold text-yellow-900">{{ analysis.criticality_breakdown.HIGH }}</div>
          <div class="text-sm text-yellow-700">High Impact</div>
        </div>
        
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div class="text-2xl font-bold text-blue-900">{{ analysis.risk_score }}</div>
          <div class="text-sm text-blue-700">Risk Score</div>
        </div>
      </div>

      <!-- Criticality Breakdown Chart -->
      <div class="mb-6">
        <h4 class="font-medium text-gray-900 mb-3">Impact by Criticality</h4>
        <div class="w-full bg-gray-200 rounded-full h-8 flex overflow-hidden">
          <div 
            :style="{ width: `${getCriticalityPercentage('CRITICAL')}%` }"
            class="bg-red-500 flex items-center justify-center text-white text-sm font-medium"
            :class="{ 'min-w-0': getCriticalityPercentage('CRITICAL') < 5 }"
          >
            <span v-if="getCriticalityPercentage('CRITICAL') >= 10">
              {{ analysis.criticality_breakdown.CRITICAL }}
            </span>
          </div>
          <div 
            :style="{ width: `${getCriticalityPercentage('HIGH')}%` }"
            class="bg-orange-500 flex items-center justify-center text-white text-sm font-medium"
            :class="{ 'min-w-0': getCriticalityPercentage('HIGH') < 5 }"
          >
            <span v-if="getCriticalityPercentage('HIGH') >= 10">
              {{ analysis.criticality_breakdown.HIGH }}
            </span>
          </div>
          <div 
            :style="{ width: `${getCriticalityPercentage('MEDIUM')}%` }"
            class="bg-yellow-500 flex items-center justify-center text-white text-sm font-medium"
            :class="{ 'min-w-0': getCriticalityPercentage('MEDIUM') < 5 }"
          >
            <span v-if="getCriticalityPercentage('MEDIUM') >= 10">
              {{ analysis.criticality_breakdown.MEDIUM }}
            </span>
          </div>
          <div 
            :style="{ width: `${getCriticalityPercentage('LOW')}%` }"
            class="bg-green-500 flex items-center justify-center text-white text-sm font-medium"
            :class="{ 'min-w-0': getCriticalityPercentage('LOW') < 5 }"
          >
            <span v-if="getCriticalityPercentage('LOW') >= 10">
              {{ analysis.criticality_breakdown.LOW }}
            </span>
          </div>
        </div>
        <div class="flex justify-between mt-2 text-sm text-gray-600">
          <span>Critical ({{ analysis.criticality_breakdown.CRITICAL }})</span>
          <span>High ({{ analysis.criticality_breakdown.HIGH }})</span>
          <span>Medium ({{ analysis.criticality_breakdown.MEDIUM }})</span>
          <span>Low ({{ analysis.criticality_breakdown.LOW }})</span>
        </div>
      </div>
    </BaseCard>

    <!-- Impacted CIs Table -->
    <BaseCard shadow="md">
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900">Impacted Configuration Items</h3>
          <div class="flex items-center space-x-2">
            <!-- Sort Options -->
            <select 
              v-model="sortBy" 
              @change="updateSort"
              class="text-sm px-3 py-1 border border-gray-300 rounded-md"
            >
              <option value="distance">Sort by Distance</option>
              <option value="criticality">Sort by Criticality</option>
              <option value="name">Sort by Name</option>
            </select>
            
            <!-- View Toggle -->
            <div class="flex bg-gray-100 rounded-lg p-1">
              <button
                @click="viewMode = 'table'"
                :class="viewMode === 'table' ? 'bg-white shadow-sm' : ''"
                class="px-3 py-1 text-sm rounded-md transition-colors"
              >
                Table
              </button>
              <button
                @click="viewMode = 'cards'"
                :class="viewMode === 'cards' ? 'bg-white shadow-sm' : ''"
                class="px-3 py-1 text-sm rounded-md transition-colors"
              >
                Cards
              </button>
            </div>
          </div>
        </div>
      </template>

      <!-- Table View -->
      <div v-if="viewMode === 'table'" class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                CI Name
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Criticality
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Distance
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Relationship Chain
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr 
              v-for="ci in sortedImpactedCIs" 
              :key="ci.ci_id"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="font-medium text-gray-900">{{ ci.ci_name }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getCriticalityBadgeColor(ci.criticality)" class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ ci.criticality }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ ci.distance }} hop{{ ci.distance > 1 ? 's' : '' }}
              </td>
              <td class="px-6 py-4 text-sm text-gray-900">
                <div class="flex flex-wrap gap-1">
                  <span 
                    v-for="(rel, index) in ci.relationship_chain" 
                    :key="index"
                    class="inline-flex items-center px-2 py-1 rounded-md text-xs bg-blue-100 text-blue-800"
                  >
                    {{ rel.replace('_', ' ') }}
                  </span>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button
                  @click="$emit('viewCI', ci.ci_id)"
                  class="text-blue-600 hover:text-blue-900"
                >
                  View Details
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Cards View -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div 
          v-for="ci in sortedImpactedCIs" 
          :key="ci.ci_id"
          class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
          @click="$emit('viewCI', ci.ci_id)"
        >
          <div class="flex items-start justify-between mb-2">
            <h4 class="font-medium text-gray-900 truncate">{{ ci.ci_name }}</h4>
            <span :class="getCriticalityBadgeColor(ci.criticality)" class="px-2 py-1 rounded-full text-xs font-medium ml-2">
              {{ ci.criticality }}
            </span>
          </div>
          
          <div class="text-sm text-gray-600 mb-3">
            Distance: {{ ci.distance }} hop{{ ci.distance > 1 ? 's' : '' }}
          </div>
          
          <div class="space-y-1">
            <div class="text-xs text-gray-500">Relationship Chain:</div>
            <div class="flex flex-wrap gap-1">
              <span 
                v-for="(rel, index) in ci.relationship_chain" 
                :key="index"
                class="inline-flex items-center px-2 py-1 rounded-md text-xs bg-blue-100 text-blue-800"
              >
                {{ rel.replace('_', ' ') }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="analysis.total_impacted === 0" class="text-center py-12">
        <CheckCircleIcon class="mx-auto h-12 w-12 text-green-400" />
        <h3 class="mt-2 text-sm font-medium text-gray-900">No Impact Detected</h3>
        <p class="mt-1 text-sm text-gray-500">
          This CI has no downstream dependencies that would be impacted by its failure.
        </p>
      </div>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ExclamationTriangleIcon, CheckCircleIcon } from '@heroicons/vue/24/outline'
import BaseCard from '@/components/ui/BaseCard.vue'
import type { ImpactAnalysis, CI } from '@/services/api'

interface Props {
  analysis: ImpactAnalysis
  sourceCI?: CI
}

const props = defineProps<Props>()

const emit = defineEmits<{
  viewCI: [ciId: string]
}>()

// State
const sortBy = ref<'distance' | 'criticality' | 'name'>('distance')
const viewMode = ref<'table' | 'cards'>('table')

// Computed
const sortedImpactedCIs = computed(() => {
  const cis = [...props.analysis.impacted_cis]
  
  switch (sortBy.value) {
    case 'distance':
      return cis.sort((a, b) => a.distance - b.distance)
    case 'criticality':
      const criticalityOrder = { 'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1 }
      return cis.sort((a, b) => 
        (criticalityOrder[b.criticality as keyof typeof criticalityOrder] || 0) - 
        (criticalityOrder[a.criticality as keyof typeof criticalityOrder] || 0)
      )
    case 'name':
      return cis.sort((a, b) => a.ci_name.localeCompare(b.ci_name))
    default:
      return cis
  }
})

// Methods
const updateSort = () => {
  // Sort will be reactive
}

const getCriticalityPercentage = (criticality: string) => {
  if (props.analysis.total_impacted === 0) return 0
  return (props.analysis.criticality_breakdown[criticality as keyof typeof props.analysis.criticality_breakdown] / props.analysis.total_impacted) * 100
}

const getRiskScoreColor = (score: number) => {
  if (score >= 50) return 'bg-red-100 text-red-800'
  if (score >= 25) return 'bg-orange-100 text-orange-800'
  if (score >= 10) return 'bg-yellow-100 text-yellow-800'
  return 'bg-green-100 text-green-800'
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
</script>