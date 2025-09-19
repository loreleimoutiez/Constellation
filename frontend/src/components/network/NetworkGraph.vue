<template>
  <div class="relative">
    <!-- Graph Container -->
    <div ref="networkContainer" class="w-full h-96 border border-gray-300 rounded-lg bg-white"></div>
    
    <!-- Controls -->
    <div class="absolute top-4 right-4 bg-white rounded-lg shadow-lg border p-3 space-y-2">
      <div class="text-sm font-medium text-gray-700">Controls</div>
      
      <!-- View Mode -->
      <div class="space-y-1">
        <label class="text-xs text-gray-600">View Mode</label>
        <select 
          v-model="viewMode" 
          @change="updateLayout"
          class="text-xs px-2 py-1 border border-gray-300 rounded"
        >
          <option value="hierarchical">Hierarchical</option>
          <option value="force">Force-directed</option>
          <option value="circular">Circular</option>
        </select>
      </div>
      
      <!-- Physics -->
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
      
      <!-- Reset View -->
      <button 
        @click="resetView"
        class="text-xs px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Reset View
      </button>
    </div>
    
    <!-- Legend -->
    <div class="absolute bottom-4 left-4 bg-white rounded-lg shadow-lg border p-3">
      <div class="text-sm font-medium text-gray-700 mb-2">Legend</div>
      <div class="space-y-1">
        <div v-for="type in ciTypes" :key="type.name" class="flex items-center space-x-2">
          <div 
            :class="type.color" 
            class="w-4 h-4 rounded-full border-2 border-gray-300"
          ></div>
          <span class="text-xs text-gray-600">{{ type.name }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Network } from 'vis-network'
import { DataSet } from 'vis-data'
import type { CI, Relationship } from '@/services/api'

interface Props {
  cis: CI[]
  relationships: Relationship[]
  selectedNodeId?: string
  height?: string
}

const props = withDefaults(defineProps<Props>(), {
  height: '400px'
})

const emit = defineEmits<{
  nodeClick: [nodeId: string]
  nodeDoubleClick: [nodeId: string]
}>()

// Refs
const networkContainer = ref<HTMLElement>()
let network: Network | null = null

// State
const viewMode = ref('force')
const physicsEnabled = ref(true)

// CI Types with colors
const ciTypes = [
  { name: 'Application', color: 'bg-blue-500' },
  { name: 'Database', color: 'bg-green-500' },
  { name: 'Hardware', color: 'bg-orange-500' },
  { name: 'Network', color: 'bg-purple-500' },
  { name: 'Service', color: 'bg-cyan-500' },
  { name: 'Storage', color: 'bg-yellow-500' },
  { name: 'Generic', color: 'bg-gray-500' }
]

// Color mapping for CI types
const getNodeColor = (ciType: string) => {
  const typeMap: Record<string, string> = {
    'APPLICATION': '#3B82F6',
    'DATABASE': '#10B981',
    'HARDWARE': '#F97316',
    'NETWORK': '#8B5CF6',
    'SERVICE': '#06B6D4',
    'STORAGE': '#EAB308',
    'GENERIC': '#6B7280'
  }
  return typeMap[ciType] || '#6B7280'
}

// Create network data
const createNetworkData = () => {
  // Create nodes from CIs
  const nodes = new DataSet(props.cis.map(ci => ({
    id: ci.id,
    label: ci.name,
    color: {
      background: getNodeColor(ci.ci_type),
      border: ci.criticality === 'CRITICAL' ? '#DC2626' : 
              ci.criticality === 'HIGH' ? '#EA580C' : '#6B7280',
      highlight: {
        background: getNodeColor(ci.ci_type),
        border: '#1F2937'
      }
    },
    borderWidth: ci.criticality === 'CRITICAL' ? 3 : 
                 ci.criticality === 'HIGH' ? 2 : 1,
    font: {
      color: '#FFFFFF',
      size: 12,
      face: 'Inter'
    },
    shape: 'dot',
    size: ci.criticality === 'CRITICAL' ? 25 : 
          ci.criticality === 'HIGH' ? 20 : 15,
    title: `${ci.name}\nType: ${ci.ci_type}\nCriticality: ${ci.criticality}\nEnvironment: ${ci.environment}`
  })))

  // Create edges from relationships
  const edges = new DataSet(props.relationships.map(rel => ({
    id: rel.id,
    from: rel.related_ci.id,
    to: rel.related_ci.id, // This will need to be adjusted based on actual relationship structure
    label: rel.type,
    color: {
      color: '#94A3B8',
      highlight: '#475569'
    },
    arrows: {
      to: {
        enabled: true,
        scaleFactor: 0.8
      }
    },
    font: {
      color: '#64748B',
      size: 10
    },
    smooth: {
      enabled: true,
      type: 'curvedCW',
      roundness: 0.2
    }
  })))

  return { nodes, edges }
}

// Network options
const getNetworkOptions = () => ({
  layout: {
    improvedLayout: true,
    hierarchical: viewMode.value === 'hierarchical' ? {
      enabled: true,
      direction: 'UD',
      sortMethod: 'directed',
      levelSeparation: 100,
      nodeSpacing: 200
    } : false
  },
  physics: {
    enabled: physicsEnabled.value,
    stabilization: {
      enabled: true,
      iterations: 100
    },
    barnesHut: {
      gravitationalConstant: -2000,
      centralGravity: 0.3,
      springLength: 95,
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
    shadow: {
      enabled: true,
      color: 'rgba(0,0,0,0.2)',
      size: 5,
      x: 2,
      y: 2
    }
  },
  edges: {
    chosen: true,
    shadow: {
      enabled: true,
      color: 'rgba(0,0,0,0.1)',
      size: 3,
      x: 1,
      y: 1
    }
  }
})

// Initialize network
const initNetwork = async () => {
  if (!networkContainer.value) return

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

  network.on('doubleClick', (params) => {
    if (params.nodes.length > 0) {
      emit('nodeDoubleClick', params.nodes[0])
    }
  })

  // Auto-fit on load
  network.once('stabilizationIterationsDone', () => {
    network?.fit()
  })
}

// Update layout
const updateLayout = () => {
  if (!network) return

  const options = getNetworkOptions()
  network.setOptions(options)
  
  if (viewMode.value === 'circular') {
    // Arrange nodes in a circle
    const nodeIds = props.cis.map(ci => ci.id)
    const positions: Record<string, { x: number, y: number }> = {}
    
    nodeIds.forEach((id, index) => {
      const angle = (index / nodeIds.length) * 2 * Math.PI
      const radius = 200
      positions[id] = {
        x: Math.cos(angle) * radius,
        y: Math.sin(angle) * radius
      }
    })
    
    // Update positions using moveNode for each node
    Object.entries(positions).forEach(([nodeId, position]) => {
      if (network) {
        network.moveNode(nodeId, position.x, position.y)
      }
    })
  }
}

// Toggle physics
const togglePhysics = () => {
  if (!network) return
  
  network.setOptions({
    physics: {
      enabled: physicsEnabled.value
    }
  })
}

// Reset view
const resetView = () => {
  if (!network) return
  network.fit()
}

// Watch for data changes
watch(() => [props.cis, props.relationships], () => {
  if (network) {
    const { nodes, edges } = createNetworkData()
    network.setData({ nodes, edges })
  }
}, { deep: true })

// Watch for selected node
watch(() => props.selectedNodeId, (nodeId) => {
  if (!network || !nodeId) return
  
  network.selectNodes([nodeId])
  network.focus(nodeId, {
    scale: 1.5,
    animation: {
      duration: 1000,
      easingFunction: 'easeInOutQuad'
    }
  })
})

// Lifecycle
onMounted(() => {
  initNetwork()
})

onUnmounted(() => {
  if (network) {
    network.destroy()
    network = null
  }
})
</script>

<style scoped>
.vis-network {
  outline: none;
}
</style>