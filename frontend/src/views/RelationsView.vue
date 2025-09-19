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
          <div ref="networkContainer" class="w-full h-[700px] border border-gray-200 rounded-lg bg-white"></div>
          
          <!-- Color Legend -->
          <div class="mt-4 bg-gray-50 rounded-lg p-4">
            <div class="flex items-center justify-between mb-3">
              <h3 class="text-sm font-medium text-gray-900">Asset Types Legend</h3>
              <div class="flex items-center space-x-2">
                <span class="text-xs text-gray-600">Click to filter</span>
                <button 
                  v-if="filteredAssetType"
                  @click="resetFilter"
                  class="text-xs px-2 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200 transition-colors"
                >
                  Clear Filter
                </button>
              </div>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 text-xs">
              <!-- Infrastructure -->
              <div class="space-y-1">
                <h4 class="font-medium text-gray-700 text-xs">Infrastructure</h4>
                <div 
                  @click="filterByAssetType('servers')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'servers' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #3B82F6;"></div>
                  <span>Servers</span>
                </div>
                <div 
                  @click="filterByAssetType('workstations')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'workstations' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #1E40AF;"></div>
                  <span>Workstations</span>
                </div>
                <div 
                  @click="filterByAssetType('network_devices')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'network_devices' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #F59E0B;"></div>
                  <span>Network Devices</span>
                </div>
                <div 
                  @click="filterByAssetType('storage_devices')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'storage_devices' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #EF4444;"></div>
                  <span>Storage</span>
                </div>
              </div>
              
              <!-- Applications -->
              <div class="space-y-1">
                <h4 class="font-medium text-gray-700 text-xs">Applications</h4>
                <div 
                  @click="filterByAssetType('applications')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'applications' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #8B5CF6;"></div>
                  <span>Applications</span>
                </div>
                <div 
                  @click="filterByAssetType('system_software')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'system_software' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #7C3AED;"></div>
                  <span>System Software</span>
                </div>
                <div 
                  @click="filterByAssetType('databases')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'databases' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #10B981;"></div>
                  <span>Databases</span>
                </div>
                <div 
                  @click="filterByAssetType('services')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'services' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #06B6D4;"></div>
                  <span>Services</span>
                </div>
              </div>
              
              <!-- People -->
              <div class="space-y-1">
                <h4 class="font-medium text-gray-700 text-xs">People & Teams</h4>
                <div 
                  @click="filterByAssetType('employees')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'employees' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #F472B6;"></div>
                  <span>Employees</span>
                </div>
                <div 
                  @click="filterByAssetType('teams')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'teams' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #EC4899;"></div>
                  <span>Teams</span>
                </div>
                <div 
                  @click="filterByAssetType('contractors')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'contractors' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #F97316;"></div>
                  <span>Contractors</span>
                </div>
              </div>
              
              <!-- Governance -->
              <div class="space-y-1">
                <h4 class="font-medium text-gray-700 text-xs">Governance</h4>
                <div 
                  @click="filterByAssetType('policies')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'policies' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #6B7280;"></div>
                  <span>Policies</span>
                </div>
                <div 
                  @click="filterByAssetType('procedures')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'procedures' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #9CA3AF;"></div>
                  <span>Procedures</span>
                </div>
                <div 
                  @click="filterByAssetType('certifications')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'certifications' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #FCD34D;"></div>
                  <span>Certifications</span>
                </div>
                <div 
                  @click="filterByAssetType('software_licenses')"
                  class="flex items-center space-x-2 cursor-pointer hover:bg-white p-1 rounded transition-colors"
                  :class="{ 'bg-white shadow-sm': filteredAssetType === 'software_licenses' }"
                >
                  <div class="w-3 h-3 rounded-full" style="background-color: #84CC16;"></div>
                  <span>Licenses</span>
                </div>
              </div>
            </div>
          </div>
          
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

    <!-- Node Details Modal -->
    <div v-if="showNodeModal && selectedNode" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <!-- Modal Header -->
        <div class="border-b border-gray-200 px-6 py-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-900">{{ selectedNode.name }}</h3>
              <p class="text-sm text-gray-600">{{ selectedNode.ci_type }}</p>
            </div>
            <button 
              @click="showNodeModal = false"
              class="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Modal Content -->
        <div class="px-6 py-4 space-y-6">
          <!-- Basic Information -->
          <div>
            <h4 class="text-md font-medium text-gray-900 mb-3">Basic Information</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Name</label>
                <p class="mt-1 text-sm text-gray-900">{{ selectedNode.name }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Type</label>
                <p class="mt-1 text-sm text-gray-900">{{ selectedNode.ci_type }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Environment</label>
                <p class="mt-1 text-sm text-gray-900">{{ selectedNode.environment }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Lifecycle State</label>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getStateColor(selectedNode.lifecycle_state)">
                  {{ selectedNode.lifecycle_state }}
                </span>
              </div>
              <div v-if="selectedNode.version" class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700">Version</label>
                <p class="mt-1 text-sm text-gray-900">{{ selectedNode.version }}</p>
              </div>
            </div>
          </div>

          <!-- Description -->
          <div v-if="selectedNode.description">
            <h4 class="text-md font-medium text-gray-900 mb-3">Description</h4>
            <p class="text-sm text-gray-700 bg-gray-50 p-3 rounded-lg">{{ selectedNode.description }}</p>
          </div>

          <!-- Attributes -->
          <div v-if="selectedNode.attributes && Object.keys(selectedNode.attributes).length > 0">
            <h4 class="text-md font-medium text-gray-900 mb-3">Attributes</h4>
            <div class="bg-gray-50 p-3 rounded-lg">
              <div class="grid grid-cols-1 gap-2">
                <div v-for="(value, key) in selectedNode.attributes" :key="key" class="flex justify-between">
                  <span class="text-sm font-medium text-gray-700">{{ key }}:</span>
                  <span class="text-sm text-gray-900">{{ value }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Relationships -->
          <div>
            <h4 class="text-md font-medium text-gray-900 mb-3">
              Relationships ({{ getNodeRelationships(selectedNode.id).length }})
            </h4>
            <div v-if="getNodeRelationships(selectedNode.id).length === 0" class="text-sm text-gray-500 italic">
              No relationships found
            </div>
            <div v-else class="space-y-2 max-h-48 overflow-y-auto">
              <div 
                v-for="rel in getNodeRelationships(selectedNode.id)" 
                :key="rel.id"
                class="flex items-center justify-between p-3 bg-gray-50 rounded-lg text-sm"
              >
                <div class="flex items-center space-x-2">
                  <span class="font-medium text-gray-900">{{ rel.type }}</span>
                  <ArrowRightIcon class="h-4 w-4 text-gray-400" />
                </div>
                <div class="text-gray-600">
                  {{ getRelatedCIName(rel, selectedNode.id) }}
                </div>
              </div>
            </div>
          </div>

          <!-- Timestamps -->
          <div>
            <h4 class="text-md font-medium text-gray-900 mb-3">Timestamps</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <label class="block font-medium text-gray-700">Created</label>
                <p class="text-gray-900">{{ formatDetailedDate(selectedNode.created_at) }}</p>
              </div>
              <div>
                <label class="block font-medium text-gray-700">Updated</label>
                <p class="text-gray-900">{{ formatDetailedDate(selectedNode.updated_at) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="border-t border-gray-200 px-6 py-4">
          <div class="flex justify-end space-x-2">
            <BaseButton variant="secondary" @click="showNodeModal = false">
              Close
            </BaseButton>
            <BaseButton @click="navigateToAsset(selectedNode.id)">
              View Details
            </BaseButton>
          </div>
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
const showNodeModal = ref(false)
const selectedNode = ref<any>(null)
const currentPage = ref(1)
const pageSize = ref(10)
const networkContainer = ref<HTMLElement>()
const network = ref<Network | null>(null)
const networkLoading = ref(true)
const layoutMode = ref('force')
const filteredAssetType = ref<string | null>(null)

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
      cis.value.map(ci => {
        const nodeRelationships = getNodeRelationships(ci.id)
        const nodeSize = Math.max(25, Math.min(50, 25 + nodeRelationships.length * 2)) // Taille basée sur le nombre de relations
        
        // Logique de filtrage simplifiée
        let nodeColor, fontColor, opacity
        
        if (!filteredAssetType.value) {
          // Pas de filtre : couleurs normales
          nodeColor = getNodeColor(ci.ci_type)
          fontColor = '#333'
          opacity = 1.0
        } else if (getAssetTypeGroup(ci.ci_type) === filteredAssetType.value) {
          // Type filtré : couleur normale
          nodeColor = getNodeColor(ci.ci_type)
          fontColor = '#333'
          opacity = 1.0
        } else {
          // Autre type : grisé
          nodeColor = '#E5E7EB'
          fontColor = '#9CA3AF'
          opacity = 0.3
        }
        
        return {
          id: ci.id,
          label: ci.name,
          title: `<div style="padding: 8px; max-width: 300px;">
            <div style="font-weight: bold; font-size: 14px; margin-bottom: 4px;">${ci.name}</div>
            <div style="color: #666; font-size: 12px; margin-bottom: 2px;"><strong>Type:</strong> ${ci.ci_type}</div>
            <div style="color: #666; font-size: 12px; margin-bottom: 2px;"><strong>Environment:</strong> ${ci.environment}</div>
            <div style="color: #666; font-size: 12px; margin-bottom: 2px;"><strong>State:</strong> ${ci.lifecycle_state}</div>
            <div style="color: #666; font-size: 12px; margin-bottom: 2px;"><strong>Relations:</strong> ${nodeRelationships.length}</div>
            ${ci.description ? `<div style="color: #666; font-size: 12px; margin-top: 6px; font-style: italic;">${ci.description}</div>` : ''}
            <div style="color: #999; font-size: 11px; margin-top: 6px; border-top: 1px solid #eee; padding-top: 4px;">Cliquez pour plus d'infos</div>
          </div>`,
          color: {
            background: nodeColor,
            border: opacity < 1 ? '#D1D5DB' : nodeColor,
            highlight: {
              background: nodeColor,
              border: nodeColor
            }
          },
          size: nodeSize,
          font: { 
            size: 12,
            color: fontColor
          }
        }
      })
    )

    // Prepare edges (Relationships) - utiliser les vraies relations
    const edgeData = relationships.value.map((rel: any) => {
      // Gérer les deux formats possibles de relations :
      // Format 1: { related_ci: {...}, direction: '...' } (interface TypeScript)
      // Format 2: { from_ci_id: '...', to_ci_id: '...' } (données réelles de l'API)
      
      let fromCI, toCI, relatedCI
      
      if (rel.related_ci && rel.direction) {
        // Format interface TypeScript avec related_ci
        relatedCI = cis.value.find(ci => ci.id === rel.related_ci.id)
        if (!relatedCI) {
          return null
        }
        
        // Pour ce format, on ne peut pas créer d'edge sans connaître le CI source
        // Il faudrait avoir plus d'informations ou adapter l'API
        return null // Temporairement on ignore ces relations
        
      } else if (rel.from_ci && rel.to_ci && rel.from_ci.id && rel.to_ci.id) {
        // Format API avec from_ci et to_ci comme objets
        fromCI = cis.value.find(ci => ci.id === rel.from_ci.id)
        toCI = cis.value.find(ci => ci.id === rel.to_ci.id)
        
        if (!fromCI || !toCI) {
          return null
        }
        
        // Logique de filtrage pour les relations
        let edgeColor, edgeWidth, edgeOpacity

        if (!filteredAssetType.value) {
          // Pas de filtre : couleurs normales
          edgeColor = getEdgeColor(rel.type)
          edgeWidth = 2
          edgeOpacity = 1.0
        } else if (getAssetTypeGroup(fromCI.ci_type) === filteredAssetType.value || 
                   getAssetTypeGroup(toCI.ci_type) === filteredAssetType.value) {
          // Au moins un des CIs connectés est du type filtré : relation visible
          edgeColor = getEdgeColor(rel.type)
          edgeWidth = 2
          edgeOpacity = 1.0
        } else {
          // Aucun des CIs n'est du type filtré : relation grisée
          edgeColor = '#E5E7EB'
          edgeWidth = 1
          edgeOpacity = 0.3
        }
        
        return {
          id: rel.id,
          from: rel.from_ci.id,
          to: rel.to_ci.id,
          label: rel.type,
          title: `<div style="padding: 6px;">
            <div style="font-weight: bold; margin-bottom: 4px;">${rel.type}</div>
            <div style="color: #666; font-size: 12px;">From: ${rel.from_ci.name}</div>
            <div style="color: #666; font-size: 12px;">To: ${rel.to_ci.name}</div>
          </div>`,
          arrows: 'to',
          color: edgeColor,
          width: edgeWidth,
          opacity: edgeOpacity
        }
        
      } else if (rel.from_ci_id && rel.to_ci_id) {
        // Format API brute avec from_ci_id/to_ci_id (garde pour compatibilité)
        fromCI = cis.value.find(ci => ci.id === rel.from_ci_id)
        toCI = cis.value.find(ci => ci.id === rel.to_ci_id)
        
        if (!fromCI || !toCI) {
          return null
        }
        
        // Logique de filtrage pour les relations
        let edgeColor, edgeWidth, edgeOpacity

        if (!filteredAssetType.value) {
          // Pas de filtre : couleurs normales
          edgeColor = getEdgeColor(rel.relationship_type || rel.type)
          edgeWidth = 2
          edgeOpacity = 1.0
        } else if (getAssetTypeGroup(fromCI.ci_type) === filteredAssetType.value || 
                   getAssetTypeGroup(toCI.ci_type) === filteredAssetType.value) {
          // Au moins un des CIs connectés est du type filtré : relation visible
          edgeColor = getEdgeColor(rel.relationship_type || rel.type)
          edgeWidth = 2
          edgeOpacity = 1.0
        } else {
          // Aucun des CIs n'est du type filtré : relation grisée
          edgeColor = '#E5E7EB'
          edgeWidth = 1
          edgeOpacity = 0.3
        }
        
        return {
          id: rel.id,
          from: rel.from_ci_id,
          to: rel.to_ci_id,
          label: rel.relationship_type || rel.type,
          title: `<div style="padding: 6px;">
            <div style="font-weight: bold; margin-bottom: 4px;">${rel.relationship_type || rel.type}</div>
            <div style="color: #666; font-size: 12px;">From: ${fromCI.name}</div>
            <div style="color: #666; font-size: 12px;">To: ${toCI.name}</div>
            ${rel.description ? `<div style="color: #666; font-size: 12px;">${rel.description}</div>` : ''}
          </div>`,
          arrows: 'to',
          color: edgeColor,
          width: edgeWidth,
          opacity: edgeOpacity
        }
        
      } else {
        // Format inconnu - essayer d'extraire les vraies propriétés
        return null
      }
    }).filter(edge => edge !== null) // Filtrer les relations null
    
    const edges = new DataSet(edgeData)
    
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
          selectedNode.value = ci
          showNodeModal.value = true
        }
      }
    })

  } catch (error) {
    console.error('Error initializing network:', error)
  } finally {
    networkLoading.value = false
  }
}

// Fonction pour mapper les types réels vers les groupes de la légende
const getAssetTypeGroup = (ciType: string): string => {
  const typeMapping: Record<string, string> = {
    // Infrastructure
    'SERVER': 'servers',
    'INFRASTRUCTURE': 'servers',
    'ENDPOINT': 'workstations',
    'WORKSTATION': 'workstations', 
    'NETWORK': 'network_devices',
    'NETWORK_DEVICE': 'network_devices',
    'STORAGE': 'storage_devices',
    'STORAGE_DEVICE': 'storage_devices',
    
    // Applications & Software
    'APPLICATION': 'applications',
    'APP': 'applications',
    'SOFTWARE': 'system_software',
    'SYSTEM': 'system_software',
    'MIDDLEWARE': 'system_software',
    
    // Data
    'DATABASE': 'databases',
    'DB': 'databases',
    'SERVICE': 'services',
    
    // People & Organization  
    'IDENTITY': 'employees',
    'PERSON': 'employees',
    'USER': 'employees',
    'TEAM': 'teams',
    'GROUP': 'teams',
    'CONTRACTOR': 'contractors',
    
    // Governance & Documents
    'POLICY': 'policies',
    'PROCEDURE': 'procedures',
    'CERTIFICATION': 'certifications',
    'CERT': 'certifications',
    'DATASET': 'procedures', // Documents/manuels
    'DOCUMENT': 'procedures',
    
    // Legal & Business
    'LICENSE': 'software_licenses',
    'LICENCE': 'software_licenses',
    'GENERIC': 'software_licenses', // La plupart des GENERIC semblent être des licences
    'CONTRACT': 'software_licenses'
  }
  
  return typeMapping[ciType.toUpperCase()] || 'generic'
}

const getNodeColor = (type: string) => {
  // Mapper le type réel vers le groupe de couleur
  const mappedType = getAssetTypeGroup(type)
  
  const colors: Record<string, string> = {
    // Infrastructure
    'servers': '#3B82F6',      // Bleu
    'workstations': '#1E40AF', // Bleu foncé
    'network_devices': '#F59E0B', // Orange
    'storage_devices': '#EF4444', // Rouge
    
    // Applications & Software
    'applications': '#8B5CF6',     // Violet
    'system_software': '#7C3AED', // Violet foncé
    'middleware': '#A855F7',       // Violet clair
    
    // Data
    'databases': '#10B981',    // Vert
    'services': '#06B6D4',     // Cyan
    
    // People & Organization
    'employees': '#F472B6',    // Rose
    'teams': '#EC4899',        // Rose foncé
    'contractors': '#F97316',  // Orange foncé
    
    // Governance
    'policies': '#6B7280',     // Gris
    'procedures': '#9CA3AF',   // Gris clair
    'certifications': '#FCD34D', // Jaune
    
    // Legal & Business
    'software_licenses': '#84CC16', // Vert lime
    'contracts': '#65A30D',         // Vert olive
    
    // Generic fallback
    'generic': '#6B7280'
  }
  return colors[mappedType] || colors['generic']
}

const getEdgeColor = (type: string) => {
  const colors: Record<string, string> = {
    'DEPENDS_ON': '#EF4444',        // Rouge - dépendance critique
    'RUNS_ON': '#3B82F6',           // Bleu - exécution/hébergement
    'HOSTS': '#10B981',             // Vert - hébergement
    'USES': '#8B5CF6',              // Violet - utilisation
    'CONNECTS_TO': '#F59E0B',       // Orange - connexion réseau
    'MEMBER_OF': '#EC4899',         // Rose - appartenance
    'RESPONSIBLE_FOR': '#DC2626',   // Rouge foncé - responsabilité
    'GOVERNED_BY': '#6B7280',       // Gris - gouvernance
    'COVERS': '#84CC16',            // Vert lime - couverture
    'DOCUMENTS': '#9CA3AF',         // Gris clair - documentation
    'PROTECTS': '#F97316',          // Orange - protection
    'INSTALLED_ON': '#06B6D4',      // Cyan - installation
    'HAS_SKILL': '#FCD34D',         // Jaune - compétence
    'COMPLIES_WITH': '#65A30D'      // Vert olive - conformité
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
            levelSeparation: 150,  // Plus d'espace vertical entre les niveaux
            nodeSpacing: 120,      // Plus d'espace horizontal entre les noeuds
            treeSpacing: 180,      // Plus d'espace entre les arbres
            blockShifting: true,
            edgeMinimization: true,
            parentCentralization: true,
            shakeTowards: 'roots'
          },
          improvedLayout: false    // Désactive l'algorithme amélioré pour éviter l'avertissement
        },
        physics: { 
          enabled: false
        },
        edges: {
          ...baseOptions.edges,
          length: 120,  // Relations plus courtes pour le mode hiérarchique
          smooth: {
            enabled: true,
            type: 'cubicBezier',
            forceDirection: 'vertical',
            roundness: 0.4
          }
        }
      }
    default: // force
      return {
        ...baseOptions,
        layout: {
          hierarchical: {
            enabled: false
          },
          improvedLayout: false    // Désactive l'algorithme amélioré pour des performances optimales
        },
        physics: {
          enabled: true,
          stabilization: { 
            iterations: 100,
            updateInterval: 25
          },
          barnesHut: {
            gravitationalConstant: -3000,  // Moins d'attraction
            centralGravity: 0.05,          // Moins de centralisation
            springLength: 300,             // Liens plus longs
            springConstant: 0.03,          // Liens plus flexibles
            damping: 0.2,                  // Plus de friction
            avoidOverlap: 1.5              // Plus d'évitement de superposition
          },
          repulsion: {
            nodeDistance: 400,             // Plus de distance entre les noeuds
            centralGravity: 0.05,
            springLength: 300,
            springConstant: 0.03,
            damping: 0.2
          }
        }
      }
  }
}

const updateLayout = () => {
  if (!network.value || !networkContainer.value) return
  
  try {
    // Détruire et recréer le network avec les nouvelles options
    // car Vis.js ne change pas toujours correctement les paramètres
    if (network.value) {
      network.value.destroy()
      network.value = null
    }
    
    // Recréer les données du network
    // Préparer les nœuds (CIs)
    const nodes = new DataSet(
      cis.value.map(ci => {
        const nodeRelationships = getNodeRelationships(ci.id)
        const nodeSize = Math.max(25, Math.min(50, 25 + nodeRelationships.length * 2))
        
        // Logique de filtrage simplifiée
        let nodeColor, fontColor, opacity
        
        if (!filteredAssetType.value) {
          // Pas de filtre : couleurs normales
          nodeColor = getNodeColor(ci.ci_type)
          fontColor = '#333'
          opacity = 1.0
        } else if (getAssetTypeGroup(ci.ci_type) === filteredAssetType.value) {
          // Type filtré : couleur normale
          nodeColor = getNodeColor(ci.ci_type)
          fontColor = '#333'
          opacity = 1.0
        } else {
          // Autre type : grisé
          nodeColor = '#E5E7EB'
          fontColor = '#9CA3AF'
          opacity = 0.3
        }
        
        return {
          id: ci.id,
          label: ci.name,
          title: `<div style="padding: 8px; max-width: 300px;">
            <div style="font-weight: bold; font-size: 14px; margin-bottom: 4px;">${ci.name}</div>
            <div style="color: #666; font-size: 12px; margin-bottom: 2px;"><strong>Type:</strong> ${ci.ci_type}</div>
            <div style="color: #666; font-size: 12px; margin-bottom: 2px;"><strong>Environment:</strong> ${ci.environment}</div>
            <div style="color: #666; font-size: 12px; margin-bottom: 2px;"><strong>State:</strong> ${ci.lifecycle_state}</div>
            <div style="color: #666; font-size: 12px; margin-bottom: 2px;"><strong>Relations:</strong> ${nodeRelationships.length}</div>
            ${ci.description ? `<div style="color: #666; font-size: 12px; margin-top: 6px; font-style: italic;">${ci.description}</div>` : ''}
            <div style="color: #999; font-size: 11px; margin-top: 6px; border-top: 1px solid #eee; padding-top: 4px;">Cliquez pour plus d'infos</div>
          </div>`,
          color: {
            background: nodeColor,
            border: opacity < 1 ? '#D1D5DB' : nodeColor,
            highlight: {
              background: nodeColor,
              border: nodeColor
            }
          },
          font: { 
            size: 14, 
            color: fontColor
          },
          borderWidth: 2,
          size: nodeSize
        }
      })
    )

    // Préparer les arêtes (Relations) - utiliser les vraies relations
    const edges = new DataSet(
      relationships.value.map((rel: any) => {
        const fromCI = cis.value.find(ci => ci.id === (rel.from_ci_id || rel.from_ci?.id || rel.source_id))
        const toCI = cis.value.find(ci => ci.id === (rel.to_ci_id || rel.to_ci?.id || rel.target_id))
        
        // Logique de filtrage pour les relations
        let edgeColor, edgeWidth, edgeOpacity
        
        if (!filteredAssetType.value) {
          // Pas de filtre : couleurs normales
          edgeColor = getEdgeColor(rel.relationship_type || rel.type)
          edgeWidth = 2
          edgeOpacity = 1.0
        } else if (getAssetTypeGroup(fromCI?.ci_type || '') === filteredAssetType.value || 
                   getAssetTypeGroup(toCI?.ci_type || '') === filteredAssetType.value) {
          // Au moins un des CIs connectés est du type filtré : relation visible
          edgeColor = getEdgeColor(rel.relationship_type || rel.type)
          edgeWidth = 2
          edgeOpacity = 1.0
        } else {
          // Aucun des CIs n'est du type filtré : relation grisée
          edgeColor = '#E5E7EB'
          edgeWidth = 1
          edgeOpacity = 0.3
        }
        
        return {
          id: rel.id,
          from: rel.from_ci_id || rel.from_ci?.id || rel.source_id,
          to: rel.to_ci_id || rel.to_ci?.id || rel.target_id,
          label: rel.relationship_type || rel.type,
          title: `<div style="padding: 6px;">
            <div style="font-weight: bold; margin-bottom: 4px;">${rel.relationship_type || rel.type}</div>
            ${rel.description ? `<div style="color: #666; font-size: 12px;">${rel.description}</div>` : ''}
          </div>`,
          arrows: 'to',
          color: edgeColor,
          font: { size: 12, color: '#666' },
          width: edgeWidth,
          opacity: edgeOpacity
        }
      })
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
          selectedNode.value = ci
          showNodeModal.value = true
        }
      }
    })
    
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

const formatDetailedDate = (date?: string) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStateColor = (state: string) => {
  const colors: Record<string, string> = {
    'active': 'bg-green-100 text-green-800',
    'inactive': 'bg-gray-100 text-gray-800',
    'deprecated': 'bg-yellow-100 text-yellow-800',
    'decommissioned': 'bg-red-100 text-red-800',
    'development': 'bg-blue-100 text-blue-800',
    'testing': 'bg-purple-100 text-purple-800'
  }
  return colors[state.toLowerCase()] || 'bg-gray-100 text-gray-800'
}

const getNodeRelationships = (nodeId: string) => {
  return relationships.value.filter((rel: any) => {
    // Gérer les différents formats de relations
    let fromId, toId
    
    if (rel.from_ci && rel.to_ci) {
      // Format avec objets from_ci/to_ci
      fromId = rel.from_ci.id
      toId = rel.to_ci.id
    } else if (rel.from_ci_id && rel.to_ci_id) {
      // Format avec IDs directs
      fromId = rel.from_ci_id
      toId = rel.to_ci_id
    } else {
      // Format avec propriétés mixtes
      fromId = rel.from_ci?.id || rel.source_id
      toId = rel.to_ci?.id || rel.target_id
    }
    
    return fromId === nodeId || toId === nodeId
  })
}

const getRelatedCIName = (relationship: any, currentNodeId: string) => {
  let fromId, toId
  
  // Gérer les différents formats de relations
  if (relationship.from_ci && relationship.to_ci) {
    // Format avec objets from_ci/to_ci
    fromId = relationship.from_ci.id
    toId = relationship.to_ci.id
  } else if (relationship.from_ci_id && relationship.to_ci_id) {
    // Format avec IDs directs
    fromId = relationship.from_ci_id
    toId = relationship.to_ci_id
  } else {
    // Format avec propriétés mixtes
    fromId = relationship.from_ci?.id || relationship.source_id
    toId = relationship.to_ci?.id || relationship.target_id
  }
  
  const relatedId = fromId === currentNodeId ? toId : fromId
  
  const relatedCI = cis.value.find(ci => ci.id === relatedId)
  return relatedCI ? relatedCI.name : 'Unknown CI'
}

const navigateToAsset = (assetId: string) => {
  // Navigation vers la page de détail de l'asset
  // TODO: Implémenter la navigation ou fermer la modal et aller à la page asset
  showNodeModal.value = false
  // this.$router.push(`/assets/${assetId}`)
  console.log('Navigate to asset:', assetId)
}

const filterByAssetType = (assetType: string) => {
  if (filteredAssetType.value === assetType) {
    // Si on clique sur le même type, on désactive le filtre
    filteredAssetType.value = null
  } else {
    // Sinon on active le filtre pour ce type
    filteredAssetType.value = assetType
  }
  
  // Recréer le réseau avec le nouveau filtre
  initializeNetwork()
}

const resetFilter = () => {
  filteredAssetType.value = null
  initializeNetwork()
}

const loadData = async () => {
  loading.value = true
  try {
    // Charger TOUS les CIs avec une limite élevée pour capturer toutes les relations
    await cmdbStore.fetchCIs({ limit: 1000 })
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