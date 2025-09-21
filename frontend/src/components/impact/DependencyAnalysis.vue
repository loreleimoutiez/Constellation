<template>
  <BaseCard shadow="md">
    <template #header>
      <h3 class="text-lg font-medium text-gray-900">Dependency Analysis</h3>
      <p class="text-sm text-gray-600 mt-1">What this CI depends on to function properly</p>
    </template>

    <!-- Overview Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div class="text-2xl font-bold text-blue-900">{{ analysis.total_dependencies }}</div>
        <div class="text-sm text-blue-700">Total Dependencies</div>
      </div>
      
      <div class="bg-purple-50 border border-purple-200 rounded-lg p-4">
        <div class="text-2xl font-bold text-purple-900">{{ analysis.max_depth_analyzed }}</div>
        <div class="text-sm text-purple-700">Max Depth Analyzed</div>
      </div>
      
      <div class="bg-cyan-50 border border-cyan-200 rounded-lg p-4">
        <div class="text-2xl font-bold text-cyan-900">{{ uniqueRelationshipTypes.length }}</div>
        <div class="text-sm text-cyan-700">Relationship Types</div>
      </div>
    </div>

    <!-- Dependency Tree/List -->
    <div v-if="analysis.total_dependencies > 0">
      <!-- Group by Distance -->
      <div class="space-y-6">
        <div 
          v-for="distance in uniqueDistances" 
          :key="distance"
          class="border border-gray-200 rounded-lg p-4"
        >
          <h4 class="font-medium text-gray-900 mb-3 flex items-center">
            <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-sm mr-2">
              Distance {{ distance }}
            </span>
            <span class="text-gray-600 text-sm">
              ({{ getDependenciesAtDistance(distance).length }} dependencies)
            </span>
          </h4>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            <div 
              v-for="dep in getDependenciesAtDistance(distance)" 
              :key="dep.ci_id"
              class="border border-gray-200 rounded-lg p-3 hover:shadow-md transition-shadow cursor-pointer bg-white"
              @click="$emit('viewCI', dep.ci_id)"
            >
              <div class="flex items-start justify-between mb-2">
                <h5 class="font-medium text-gray-900 truncate">{{ dep.ci_name }}</h5>
                <span :class="getCriticalityBadgeColor(dep.criticality)" class="px-2 py-1 rounded-full text-xs font-medium ml-2">
                  {{ dep.criticality }}
                </span>
              </div>
              
              <div class="space-y-2">
                <div class="text-xs text-gray-500">Relationship Chain:</div>
                <div class="flex flex-wrap gap-1">
                  <span 
                    v-for="(rel, index) in dep.relationship_chain" 
                    :key="index"
                    class="inline-flex items-center px-2 py-1 rounded-md text-xs"
                    :class="getRelationshipColor(rel)"
                  >
                    {{ formatRelationshipType(rel) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <ShieldCheckIcon class="mx-auto h-12 w-12 text-green-400" />
      <h3 class="mt-2 text-sm font-medium text-gray-900">No Dependencies Found</h3>
      <p class="mt-1 text-sm text-gray-500">
        This CI appears to be self-contained with no external dependencies.
      </p>
    </div>

    <!-- Relationship Type Legend -->
    <div v-if="analysis.total_dependencies > 0" class="mt-6 border-t border-gray-200 pt-4">
      <h4 class="text-sm font-medium text-gray-900 mb-3">Relationship Types</h4>
      <div class="flex flex-wrap gap-2">
        <div 
          v-for="type in uniqueRelationshipTypes" 
          :key="type"
          class="flex items-center space-x-2"
        >
          <div :class="getRelationshipColor(type)" class="px-2 py-1 rounded-md text-xs">
            {{ formatRelationshipType(type) }}
          </div>
          <span class="text-sm text-gray-600">
            ({{ getRelationshipTypeCount(type) }})
          </span>
        </div>
      </div>
    </div>
  </BaseCard>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ShieldCheckIcon } from '@heroicons/vue/24/outline'
import BaseCard from '@/components/ui/BaseCard.vue'

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

interface Props {
  analysis: DependencyAnalysis
}

const props = defineProps<Props>()

const emit = defineEmits<{
  viewCI: [ciId: string]
}>()

// Computed
const uniqueDistances = computed(() => {
  const distances = props.analysis.dependencies.map(dep => dep.distance)
  return [...new Set(distances)].sort((a, b) => a - b)
})

const uniqueRelationshipTypes = computed(() => {
  const types = props.analysis.dependencies.flatMap(dep => dep.relationship_chain)
  return [...new Set(types)]
})

// Methods
const getDependenciesAtDistance = (distance: number) => {
  return props.analysis.dependencies.filter(dep => dep.distance === distance)
}

const getRelationshipTypeCount = (type: string) => {
  return props.analysis.dependencies.filter(dep => 
    dep.relationship_chain.includes(type)
  ).length
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

const getRelationshipColor = (relationshipType: string) => {
  const colors = {
    'DEPENDS_ON': 'bg-blue-100 text-blue-800',
    'RUNS_ON': 'bg-green-100 text-green-800',
    'HOSTS': 'bg-purple-100 text-purple-800',
    'USES': 'bg-orange-100 text-orange-800',
    'CONNECTS_TO': 'bg-cyan-100 text-cyan-800',
    'COMMUNICATES_WITH': 'bg-indigo-100 text-indigo-800'
  }
  return colors[relationshipType as keyof typeof colors] || 'bg-gray-100 text-gray-800'
}

const formatRelationshipType = (type: string) => {
  return type.replace(/_/g, ' ').toLowerCase().replace(/\b\w/g, l => l.toUpperCase())
}
</script>