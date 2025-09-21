<template>
  <BaseCard shadow="md">
    <template #header>
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-medium text-gray-900">Impact Network Visualization</h3>
        <div class="flex items-center space-x-2">
          <!-- Analysis Type Toggle -->
          <div class="flex bg-gray-100 rounded-lg p-1">
            <button
              @click="analysisType = 'impact'"
              :class="analysisType === 'impact' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-600'"
              class="px-3 py-1 text-sm rounded-md transition-colors"
            >
              Impact
            </button>
            <button
              @click="analysisType = 'dependencies'"
              :class="analysisType === 'dependencies' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-600'"
              class="px-3 py-1 text-sm rounded-md transition-colors"
            >
              Dependencies
            </button>
          </div>
          
          <!-- Refresh Button -->
          <button
            @click="refreshVisualization"
            :disabled="isLoading"
            class="px-3 py-1 text-sm bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50"
          >
            <ArrowPathIcon v-if="isLoading" class="h-4 w-4 animate-spin" />
            <span v-else>Refresh</span>
          </button>
        </div>
      </div>
    </template>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex items-center justify-center py-12">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
        <p class="mt-4 text-sm text-gray-600">Building network visualization...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <ExclamationCircleIcon class="mx-auto h-12 w-12 text-red-400" />
      <h3 class="mt-2 text-sm font-medium text-gray-900">Visualization Error</h3>
      <p class="mt-1 text-sm text-gray-500">{{ error }}</p>
      <button
        @click="refreshVisualization"
        class="mt-4 px-4 py-2 text-sm bg-blue-500 text-white rounded-md hover:bg-blue-600"
      >
        Try Again
      </button>
    </div>

    <!-- Network Visualization -->
    <div v-else class="relative">
      <!-- Network Graph -->
      <div ref="networkContainer" class="w-full h-96 border border-gray-300 rounded-lg bg-white"></div>
      
      <!-- Network Controls -->
      <div class="absolute top-4 right-4 bg-white rounded-lg shadow-lg border p-3 space-y-2">
        <div class="text-sm font-medium text-gray-700">Controls</div>
        
        <!-- Layout Mode -->
        <div class="space-y-1">
          <label class="text-xs text-gray-600">Layout</label>
          <select 
            v-model="layoutMode" 
            @change="updateLayout"
            class="text-xs px-2 py-1 border border-gray-300 rounded"
          >
            <option value="hierarchical">Hierarchical</option>
            <option value="radial">Radial</option>
            <option value="force">Force-directed</option>
          </select>
        </div>
        
        <!-- Physics Toggle -->
        <div class="flex items-center space-x-2">
          <input 
            id="physics" 
            v-model="physicsEnabled" 
            type="checkbox" 
            @change="togglePhysics"
            class="text-xs"
          >
          <label for="physics" class="text-xs text-gray-600">Physics</label>
        </div>
        
        <!-- Distance Filter -->
        <div class="space-y-1">
          <label class="text-xs text-gray-600">Max Distance</label>
          <select 
            v-model="maxDistance" 
            @change="filterByDistance"
            class="text-xs px-2 py-1 border border-gray-300 rounded"
          >
            <option value="1">1 hop</option>
            <option value="2">2 hops</option>
            <option value="3">3 hops</option>
            <option value="999">All</option>
          </select>
        </div>
        
        <!-- Reset View -->
        <button 
          @click="resetView"
          class="w-full text-xs px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Reset View
        </button>
      </div>
      
      <!-- Impact Legend -->
      <div class="absolute bottom-4 left-4 bg-white rounded-lg shadow-lg border p-3">
        <div class="text-sm font-medium text-gray-700 mb-2">Legend</div>
        <div class="space-y-2">
          <!-- Source Node -->
          <div class="flex items-center space-x-2">
            <div class="w-4 h-4 rounded-full bg-blue-600 border-2 border-blue-800"></div>
            <span class="text-xs text-gray-600">Source CI</span>
          </div>
          
          <!-- Criticality Levels -->
          <div class="space-y-1">
            <div class="flex items-center space-x-2">
              <div class="w-4 h-4 rounded-full bg-red-500 border-2 border-red-700"></div>
              <span class="text-xs text-gray-600">Critical</span>
            </div>
            <div class="flex items-center space-x-2">
              <div class="w-4 h-4 rounded-full bg-orange-500 border-2 border-orange-700"></div>
              <span class="text-xs text-gray-600">High</span>
            </div>
            <div class="flex items-center space-x-2">
              <div class="w-4 h-4 rounded-full bg-yellow-500 border-2 border-yellow-700"></div>
              <span class="text-xs text-gray-600">Medium</span>
            </div>
            <div class="flex items-center space-x-2">
              <div class="w-4 h-4 rounded-full bg-green-500 border-2 border-green-700"></div>
              <span class="text-xs text-gray-600">Low</span>
            </div>
          </div>
          
          <!-- Distance Indicator -->
          <div class="border-t pt-2 mt-2">
            <div class="text-xs text-gray-500 mb-1">Distance from source:</div>
            <div class="flex items-center space-x-1">
              <div class="w-3 h-3 rounded-full border-2 border-gray-400"></div>
              <span class="text-xs text-gray-500">1 hop</span>
            </div>
            <div class="flex items-center space-x-1">
              <div class="w-4 h-4 rounded-full border-2 border-gray-400"></div>
              <span class="text-xs text-gray-500">2 hops</span>
            </div>
            <div class="flex items-center space-x-1">
              <div class="w-5 h-5 rounded-full border-2 border-gray-400"></div>
              <span class="text-xs text-gray-500">3+ hops</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Network Stats -->
    <div v-if="!isLoading && !error" class="mt-4 grid grid-cols-3 gap-4 pt-4 border-t border-gray-200">
      <div class="text-center">
        <div class="text-lg font-bold text-gray-900">{{ visibleNodes.length }}</div>
        <div class="text-sm text-gray-600">Visible Nodes</div>
      </div>
      <div class="text-center">
        <div class="text-lg font-bold text-gray-900">{{ visibleEdges.length }}</div>
        <div class="text-sm text-gray-600">Visible Edges</div>
      </div>
      <div class="text-center">
        <div class="text-lg font-bold text-gray-900">{{ maxDistance === 999 ? 'All' : maxDistance }}</div>
        <div class="text-sm text-gray-600">Max Distance</div>
      </div>
    </div>
  </BaseCard>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'
import { Network } from 'vis-network'
import { DataSet } from 'vis-data'
import { ArrowPathIcon, ExclamationCircleIcon } from '@heroicons/vue/24/outline'
import BaseCard from '@/components/ui/BaseCard.vue'
import type { ImpactAnalysis, CI } from '@/services/api'

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
  sourceCI: CI
  impactAnalysis?: ImpactAnalysis
  dependencyAnalysis?: DependencyAnalysis
  isLoading?: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  nodeClick: [nodeId: string]
  refresh: []
}>()

// Refs
const networkContainer = ref<HTMLElement>()
let network: Network | null = null

// State
const analysisType = ref<'impact' | 'dependencies'>('impact')
const layoutMode = ref('hierarchical')
const physicsEnabled = ref(true)
const maxDistance = ref(3)
const error = ref<string | null>(null)

// Computed
const currentAnalysis = computed(() => {
  return analysisType.value === 'impact' ? props.impactAnalysis : props.dependencyAnalysis
})

const visibleNodes = ref<any[]>([])
const visibleEdges = ref<any[]>([])

// Methods
const getNodeColor = (criticality: string, isSource = false) => {
  if (isSource) {
    return {
      background: '#2563EB',
      border: '#1D4ED8',
      highlight: { background: '#3B82F6', border: '#1E40AF' }
    }
  }
  
  const colors = {
    'CRITICAL': { background: '#EF4444', border: '#DC2626' },
    'HIGH': { background: '#F97316', border: '#EA580C' },
    'MEDIUM': { background: '#EAB308', border: '#CA8A04' },
    'LOW': { background: '#10B981', border: '#059669' }
  }
  
  const color = colors[criticality as keyof typeof colors] || colors.LOW
  return {
    ...color,
    highlight: { background: color.background, border: '#1F2937' }
  }
}

const getNodeSize = (distance: number, isSource = false) => {
  if (isSource) return 30
  
  switch (distance) {
    case 1: return 20
    case 2: return 25
    case 3: return 30
    default: return 35
  }
}

const createNetworkData = () => {
  if (!currentAnalysis.value) {
    return { nodes: new DataSet([]), edges: new DataSet([]) }
  }
  
  const nodes: any[] = []
  const edges: any[] = []
  
  // Add source node
  nodes.push({
    id: props.sourceCI.id,
    label: props.sourceCI.name,
    color: getNodeColor(props.sourceCI.criticality, true),
    size: getNodeSize(0, true),
    borderWidth: 3,
    font: { color: '#1F2937', size: 12, face: 'Inter', strokeWidth: 2, strokeColor: '#FFFFFF' },
    shape: 'dot',
    title: `${props.sourceCI.name} (Source)\nType: ${props.sourceCI.ci_type}\nCriticality: ${props.sourceCI.criticality}`,
    distance: 0,
    criticality: props.sourceCI.criticality
  })
  
  // Add related nodes
  const relatedCIs = analysisType.value === 'impact' 
    ? props.impactAnalysis?.impacted_cis || []
    : props.dependencyAnalysis?.dependencies || []
  
  relatedCIs.forEach(ci => {
    if (ci.distance <= maxDistance.value) {
      nodes.push({
        id: ci.ci_id,
        label: ci.ci_name,
        color: getNodeColor(ci.criticality),
        size: getNodeSize(ci.distance),
        borderWidth: ci.criticality === 'CRITICAL' ? 3 : 2,
        font: { color: '#1F2937', size: 10, face: 'Inter', strokeWidth: 1, strokeColor: '#FFFFFF' },
        shape: 'dot',
        title: `${ci.ci_name}\nCriticality: ${ci.criticality}\nDistance: ${ci.distance} hop${ci.distance > 1 ? 's' : ''}`,
        distance: ci.distance,
        criticality: ci.criticality
      })
      
      // Create edge
      const edgeId = `${props.sourceCI.id}-${ci.ci_id}`
      edges.push({
        id: edgeId,
        from: analysisType.value === 'impact' ? props.sourceCI.id : ci.ci_id,
        to: analysisType.value === 'impact' ? ci.ci_id : props.sourceCI.id,
        color: { color: '#94A3B8', highlight: '#475569' },
        arrows: { to: { enabled: true, scaleFactor: 0.8 } },
        smooth: { enabled: true, type: 'curvedCW', roundness: 0.2 },
        width: Math.max(1, 4 - ci.distance),
        title: `${ci.relationship_chain.join(' → ')}`
      })
    }
  })
  
  visibleNodes.value = nodes
  visibleEdges.value = edges
  
  return {
    nodes: new DataSet(nodes),
    edges: new DataSet(edges)
  }
}

const getNetworkOptions = () => ({
  layout: {
    improvedLayout: true,
    hierarchical: layoutMode.value === 'hierarchical' ? {
      enabled: true,
      direction: analysisType.value === 'impact' ? 'UD' : 'DU',
      sortMethod: 'directed',
      levelSeparation: 150,
      nodeSpacing: 200,
      treeSpacing: 300
    } : false
  },
  physics: {
    enabled: physicsEnabled.value,
    stabilization: { enabled: true, iterations: 100 },
    barnesHut: {
      gravitationalConstant: -2000,
      centralGravity: 0.3,
      springLength: 120,
      springConstant: 0.04,
      damping: 0.09
    }
  },
  interaction: {
    hover: true,
    tooltipDelay: 200,
    zoomView: true,
    dragView: true
  },
  nodes: {
    chosen: true,
    shadow: { enabled: true, color: 'rgba(0,0,0,0.2)', size: 5, x: 2, y: 2 }
  },
  edges: {
    chosen: true,
    shadow: { enabled: true, color: 'rgba(0,0,0,0.1)', size: 3, x: 1, y: 1 }
  }
})

const initNetwork = async () => {
  if (!networkContainer.value) return
  
  try {
    await nextTick()
    
    const { nodes, edges } = createNetworkData()
    const options = getNetworkOptions()
    
    network = new Network(networkContainer.value, { nodes, edges }, options)
    
    // Event listeners
    network.on('click', (params) => {
      if (params.nodes.length > 0) {
        emit('nodeClick', params.nodes[0])
      }
    })
    
    // Auto-fit when stabilized
    network.once('stabilizationIterationsDone', () => {
      network?.fit()
    })
    
    error.value = null
  } catch (err) {
    error.value = 'Failed to initialize network visualization'
    console.error('Network initialization error:', err)
  }
}

const updateLayout = () => {
  if (!network) return
  
  const options = getNetworkOptions()
  network.setOptions(options)
  
  if (layoutMode.value === 'radial') {
    arrangeRadially()
  }
}

const arrangeRadially = () => {
  if (!network || !currentAnalysis.value) return
  
  const positions: Record<string, { x: number, y: number }> = {}
  
  // Center the source node
  positions[props.sourceCI.id] = { x: 0, y: 0 }
  
  // Arrange nodes by distance in concentric circles
  const relatedCIs = analysisType.value === 'impact' 
    ? props.impactAnalysis?.impacted_cis || []
    : props.dependencyAnalysis?.dependencies || []
  
  const byDistance = relatedCIs
    .filter(ci => ci.distance <= maxDistance.value)
    .reduce((acc, ci) => {
      if (!acc[ci.distance]) acc[ci.distance] = []
      acc[ci.distance].push(ci)
      return acc
    }, {} as Record<number, any[]>)
  
  Object.entries(byDistance).forEach(([distance, cis]) => {
    const radius = parseInt(distance) * 150
    cis.forEach((ci, index) => {
      const angle = (index / cis.length) * 2 * Math.PI
      positions[ci.ci_id] = {
        x: Math.cos(angle) * radius,
        y: Math.sin(angle) * radius
      }
    })
  })
  
  // Apply positions
  Object.entries(positions).forEach(([nodeId, position]) => {
    network?.moveNode(nodeId, position.x, position.y)
  })
}

const togglePhysics = () => {
  if (!network) return
  network.setOptions({ physics: { enabled: physicsEnabled.value } })
}

const filterByDistance = () => {
  if (!network) return
  const { nodes, edges } = createNetworkData()
  network.setData({ nodes, edges })
}

const resetView = () => {
  if (!network) return
  network.fit()
}

const refreshVisualization = () => {
  emit('refresh')
  if (network) {
    const { nodes, edges } = createNetworkData()
    network.setData({ nodes, edges })
  }
}

// Watch for changes
watch(() => [props.impactAnalysis, props.dependencyAnalysis], () => {
  if (network) {
    const { nodes, edges } = createNetworkData()
    network.setData({ nodes, edges })
  }
}, { deep: true })

watch(analysisType, () => {
  if (network) {
    const { nodes, edges } = createNetworkData()
    network.setData({ nodes, edges })
    updateLayout()
  }
})

// Lifecycle
onMounted(() => {
  if (!props.isLoading) {
    initNetwork()
  }
})

onUnmounted(() => {
  if (network) {
    network.destroy()
    network = null
  }
})

// Watch for loading state changes
watch(() => props.isLoading, (loading) => {
  if (!loading && !network) {
    nextTick(() => initNetwork())
  }
})
</script>

<style scoped>
.vis-network {
  outline: none;
}
</style>