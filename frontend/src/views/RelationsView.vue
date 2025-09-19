<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="bg-white shadow">
      <div class="px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">Relations</h1>
              <p class="mt-2 text-gray-600">Visualize dependencies and relationships between your assets</p>
            </div>
            <BaseButton @click="showCreateRelationModal = true">
              <PlusIcon class="h-5 w-5 mr-2" />
              Add Relation
            </BaseButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Network Visualization -->
    <BaseCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900">Network Visualization</h2>
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <label class="text-sm text-gray-600">Layout:</label>
              <select 
                v-model="layoutMode" 
                @change="updateLayout"
                class="text-sm px-2 py-1 border border-gray-300 rounded"
              >
                <option value="force">Force-directed</option>
                <option value="hierarchical">Hierarchical</option>
                <option value="circular">Circular</option>
              </select>
            </div>
            <span class="text-sm text-gray-600">
              {{ cis.length }} Assets • {{ relationships.length }} Relations
            </span>
          </div>
        </div>
      </template>
      
      <!-- Network Graph Container -->
      <div class="relative">
        <!-- Desktop Network Visualization -->
        <div class="hidden lg:block">
          <div ref="networkContainer" class="w-full h-[600px] border border-gray-200 rounded-lg bg-white"></div>
          
          <!-- Loading Overlay -->
          <div v-if="networkLoading" class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center rounded-lg">
            <div class="text-center">
              <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-constellation-600"></div>
              <p class="mt-2 text-gray-600">Building network...</p>
            </div>
          </div>
          
          <!-- Empty State -->
          <div v-if="!networkLoading && cis.length === 0" class="absolute inset-0 flex items-center justify-center">
            <div class="text-center">
              <ServerIcon class="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <h3 class="text-lg font-medium text-gray-900 mb-2">No Assets Found</h3>
              <p class="text-gray-600 mb-4">Create some assets first to visualize their relationships</p>
              <BaseButton @click="$router.push('/assets/new')">
                Create Asset
              </BaseButton>
            </div>
          </div>
        </div>
        
        <!-- Mobile Information Message -->
        <div class="lg:hidden bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-blue-800">
                Visualisation réseau disponible sur desktop uniquement
              </h3>
              <div class="mt-2 text-sm text-blue-700">
                <p>La visualisation interactive du réseau d'assets nécessite un écran plus large pour une expérience optimale. Veuillez utiliser un ordinateur de bureau ou une tablette en mode paysage.</p>
              </div>
              <div class="mt-4">
                <div class="flex">
                  <BaseButton variant="secondary" size="sm" @click="$router.push('/assets')">
                    <svg class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                    Voir la liste des Assets
                  </BaseButton>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </BaseCard>

    <!-- Relationships List -->
    <BaseCard>
      <template #header>
        <h2 class="text-lg font-semibold text-gray-900">Recent Relationships</h2>
      </template>
      
      <div v-if="loading" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-constellation-600"></div>
        <p class="mt-2 text-gray-600">Loading relationships...</p>
      </div>

      <div v-else-if="relationships.length === 0" class="text-center py-8">
        <LinkIcon class="mx-auto h-12 w-12 text-gray-400" />
        <p class="mt-2 text-gray-600">No relationships found</p>
        <BaseButton class="mt-4" @click="showCreateRelationModal = true">
          Create your first relationship
        </BaseButton>
      </div>

      <div v-else class="overflow-hidden">
        <div class="space-y-4">
          <div 
            v-for="relationship in paginatedRelationships" 
            :key="relationship.id"
            class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
          >
            <div class="flex items-center space-x-4">
              <div class="flex items-center space-x-2">
                <ArrowRightIcon class="h-4 w-4 text-gray-400" />
                <span class="font-medium text-gray-900">{{ relationship.type }}</span>
              </div>
              <div class="text-sm text-gray-600">
                Direction: {{ relationship.direction }}
              </div>
            </div>
            
            <div class="flex items-center space-x-4">
              <div class="text-sm">
                <span class="text-gray-600">Related to:</span>
                <span class="font-medium text-gray-900 ml-1">{{ relationship.related_ci.name }}</span>
              </div>
              <div class="text-xs text-gray-500">
                {{ formatDate(relationship.created_at) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="flex items-center justify-between mt-6 pt-4 border-t border-gray-200">
          <p class="text-sm text-gray-700">
            Showing {{ (currentPage - 1) * pageSize + 1 }} to {{ Math.min(currentPage * pageSize, normalizedRelationships.length) }} of {{ normalizedRelationships.length }} relationships
          </p>
          <div class="flex space-x-2">
            <BaseButton
              variant="secondary"
              size="sm"
              :disabled="currentPage === 1"
              @click="currentPage--"
            >
              Previous
            </BaseButton>
            <BaseButton
              variant="secondary"
              size="sm"
              :disabled="currentPage === totalPages"
              @click="currentPage++"
            >
              Next
            </BaseButton>
          </div>
        </div>
      </div>
    </BaseCard>

    <!-- Create Relationship Modal Placeholder -->
    <div v-if="showCreateRelationModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Create Relationship</h3>
        <p class="text-gray-600 mb-4">Relationship creation form will be implemented here</p>
        <div class="flex justify-end space-x-2">
          <BaseButton variant="secondary" @click="showCreateRelationModal = false">
            Cancel
          </BaseButton>
          <BaseButton @click="showCreateRelationModal = false">
            Create
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { Network } from 'vis-network'
import { DataSet } from 'vis-data'
import { useCMDBStore } from '@/stores/cmdb'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import {
  PlusIcon,
  ServerIcon,
  LinkIcon,
  ArrowRightIcon,
} from '@heroicons/vue/24/outline'

const cmdbStore = useCMDBStore()

// State
const loading = ref(false)
const showCreateRelationModal = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const networkContainer = ref<HTMLElement>()
const network = ref<Network | null>(null)
const networkLoading = ref(true)
const layoutMode = ref('force')

// Computed
const cis = computed(() => cmdbStore.cis)
const relationships = computed(() => cmdbStore.relationships)

// Normalize relationships to handle both formats (related_ci vs from_ci/to_ci)
const normalizedRelationships = computed(() => {
  return relationships.value.map((rel: any) => {
    // Si c'est le nouveau format avec from_ci/to_ci, normaliser vers related_ci
    if (rel.from_ci || rel.to_ci) {
      // Déterminer quel CI est le "related" selon le contexte
      // Pour la vue générale, on prend to_ci comme related par défaut
      const related_ci = rel.to_ci || rel.from_ci
      return {
        ...rel,
        related_ci: related_ci,
        direction: rel.from_ci && rel.to_ci ? 'outgoing' : 'unknown'
      }
    }
    // Sinon, retourner tel quel (format existant)
    return rel
  })
})

const totalPages = computed(() => Math.ceil(normalizedRelationships.value.length / pageSize.value))

const paginatedRelationships = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return normalizedRelationships.value.slice(start, end)
})

// Network visualization
const initializeNetwork = async () => {
  // Ne charger la visualisation que sur desktop (lg breakpoint et plus)
  if (window.innerWidth < 1024) {
    console.log('Skipping network initialization on mobile/tablet')
    networkLoading.value = false
    return
  }
  
  if (!networkContainer.value) {
    console.warn('Network container not available')
    networkLoading.value = false
    return
  }
  
  if (cis.value.length === 0) {
    console.log('No CIs available for network visualization')
    networkLoading.value = false
    return
  }
  
  networkLoading.value = true
  
  try {
    // Prepare nodes (CIs)
    const nodes = new DataSet(
      cis.value.map(ci => ({
        id: ci.id,
        label: ci.name,
        title: `${ci.ci_type}: ${ci.name}\nEnvironment: ${ci.environment}\nState: ${ci.lifecycle_state}`,
        color: getNodeColor(ci.ci_type),
        size: 30,
        font: { size: 12 }
      }))
    )

    // For now, create some dummy relationships since backend might not have them yet
    const dummyRelations = []
    if (cis.value.length > 1) {
      for (let i = 0; i < Math.min(cis.value.length - 1, 5); i++) {
        dummyRelations.push({
          id: `rel-${i}`,
          sourceId: cis.value[i].id,
          targetId: cis.value[i + 1].id,
          type: 'depends_on',
          description: 'Example relationship'
        })
      }
    }

    // Prepare edges (Relationships)
    const edges = new DataSet(
      dummyRelations.map(rel => ({
        id: rel.id,
        from: rel.sourceId,
        to: rel.targetId,
        label: rel.type,
        title: `${rel.type}: ${rel.description || 'No description'}`,
        arrows: 'to',
        color: getEdgeColor(rel.type),
        width: 2
      }))
    )

    const data = { nodes, edges }
    const options = getNetworkOptions()

    // Destroy existing network
    if (network.value) {
      network.value.destroy()
      network.value = null
    }
    
    // Create new network
    network.value = new Network(networkContainer.value, data, options)
    
    // Add event listeners
    network.value.on('click', (params) => {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0]
        const ci = cis.value.find(c => c.id === nodeId)
        if (ci) {
          console.log('Clicked CI:', ci)
          // TODO: Navigate to CI detail or show modal
        }
      }
    })

    console.log('Network initialized successfully')

  } catch (error) {
    console.error('Error initializing network:', error)
  } finally {
    networkLoading.value = false
  }
}

const getNodeColor = (type: string) => {
  const colors: Record<string, string> = {
    'server': '#3B82F6',
    'database': '#10B981',
    'application': '#8B5CF6',
    'network': '#F59E0B',
    'storage': '#EF4444',
    'service': '#06B6D4'
  }
  return colors[type] || '#6B7280'
}

const getEdgeColor = (type: string) => {
  const colors: Record<string, string> = {
    'depends_on': '#EF4444',
    'connects_to': '#3B82F6',
    'hosts': '#10B981',
    'uses': '#8B5CF6',
    'communicates_with': '#F59E0B'
  }
  return colors[type] || '#6B7280'
}

const getNetworkOptions = () => {
  const baseOptions = {
    interaction: {
      hover: true,
      tooltipDelay: 200
    },
    nodes: {
      borderWidth: 2,
      borderWidthSelected: 4,
      chosen: true,
      shape: 'dot'
    },
    edges: {
      chosen: true,
      hoverWidth: 4,
      selectionWidth: 4,
      smooth: {
        enabled: true,
        type: 'continuous',
        roundness: 0.5
      }
    }
  }

  switch (layoutMode.value) {
    case 'hierarchical':
      return {
        ...baseOptions,
        layout: {
          hierarchical: {
            enabled: true,
            direction: 'UD',
            sortMethod: 'directed',
            levelSeparation: 150,
            nodeSpacing: 100
          }
        },
        physics: { 
          enabled: false
        }
      }
    case 'circular':
      return {
        ...baseOptions,
        layout: {
          hierarchical: {
            enabled: false
          }
        },
        physics: { 
          enabled: false 
        }
      }
    default: // force
      return {
        ...baseOptions,
        layout: {
          hierarchical: {
            enabled: false
          }
        },
        physics: {
          enabled: true,
          stabilization: { 
            iterations: 100,
            updateInterval: 50
          },
          barnesHut: {
            gravitationalConstant: -2000,
            centralGravity: 0.3,
            springLength: 95,
            springConstant: 0.04,
            damping: 0.09
          }
        }
      }
  }
}

const updateLayout = () => {
  if (!network.value || !networkContainer.value) return
  
  try {
    console.log(`Switching to layout: ${layoutMode.value}`)
    
    // Pour certains changements de layout, il faut complètement recréer le network
    // car Vis.js ne change pas toujours correctement les paramètres
    if (layoutMode.value === 'force' || layoutMode.value === 'hierarchical') {
      // Détruire et recréer le network avec les nouvelles options
      if (network.value) {
        network.value.destroy()
        network.value = null
      }
      
      // Recréer les données du network
      // Préparer les nœuds (CIs)
      const nodes = new DataSet(
        cis.value.map(ci => ({
          id: ci.id,
          label: ci.name,
          title: `${ci.ci_type}: ${ci.name}\nEnvironment: ${ci.environment}\nState: ${ci.lifecycle_state}`,
          color: getNodeColor(ci.ci_type),
          font: { size: 14, color: '#333' },
          borderWidth: 2,
          size: 25
        }))
      )

      // For now, create some dummy relationships since backend might not have them yet
      const dummyRelations = []
      if (cis.value.length > 1) {
        for (let i = 0; i < Math.min(cis.value.length - 1, 5); i++) {
          dummyRelations.push({
            id: `rel-${i}`,
            sourceId: cis.value[i].id,
            targetId: cis.value[i + 1].id,
            type: 'depends_on',
            description: 'Example relationship'
          })
        }
      }

      // Préparer les arêtes (Relations)
      const edges = new DataSet(
        dummyRelations.map(rel => ({
          id: rel.id,
          from: rel.sourceId,
          to: rel.targetId,
          label: rel.type,
          title: `${rel.type}: ${rel.description || 'No description'}`,
          arrows: 'to',
          color: getEdgeColor(rel.type),
          width: 2
        }))
      )

      const data = { nodes, edges }
      const options = getNetworkOptions()
      network.value = new Network(networkContainer.value, data, options)
      
      // Remettre les event listeners
      network.value.on('click', (params) => {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0]
          const ci = cis.value.find(c => c.id === nodeId)
          if (ci) {
            console.log('Clicked CI:', ci)
          }
        }
      })
      
      console.log(`Network recreated with ${layoutMode.value} layout`)
      
    } else if (layoutMode.value === 'circular' && cis.value.length > 0) {
      // Pour circular, on peut juste modifier les positions
      const options = getNetworkOptions()
      network.value.setOptions(options)
      
      // Arrange nodes in a circle
      const nodeIds = cis.value.map(ci => ci.id)
      const angleStep = (2 * Math.PI) / nodeIds.length
      const radius = 200
      
      // Move each node to circular position
      nodeIds.forEach((id, index) => {
        const angle = index * angleStep
        const x = radius * Math.cos(angle)
        const y = radius * Math.sin(angle)
        if (network.value) {
          network.value.moveNode(id, x, y)
        }
      })
    }
    
  } catch (error) {
    console.error('Error updating layout:', error)
    // En cas d'erreur, réinitialiser complètement
    initializeNetwork()
  }
}

// Methods
const formatDate = (date?: string) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const loadData = async () => {
  loading.value = true
  try {
    await cmdbStore.fetchCIs()
    await cmdbStore.fetchAllRelationships()
    await nextTick()
    initializeNetwork()
  } catch (error) {
    console.error('Failed to load data:', error)
  } finally {
    loading.value = false
  }
}

// Lifecycle
let handleResize: () => void

onMounted(() => {
  loadData()
  
  // Listener pour redimensionnement de fenêtre
  handleResize = () => {
    // Si on passe de mobile à desktop ou vice-versa, recharger la visualisation
    const isDesktop = window.innerWidth >= 1024
    const hasNetwork = network.value !== null
    
    if (isDesktop && !hasNetwork && cis.value.length > 0) {
      // Passer en mode desktop : initialiser le réseau
      initializeNetwork()
    } else if (!isDesktop && hasNetwork) {
      // Passer en mode mobile : détruire le réseau
      if (network.value) {
        network.value.destroy()
        network.value = null
      }
      networkLoading.value = false
    }
  }
  
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (handleResize) {
    window.removeEventListener('resize', handleResize)
  }
  if (network.value) {
    network.value.destroy()
  }
})
</script>