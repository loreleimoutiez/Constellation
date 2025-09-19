<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="bg-white shadow">
      <div class="px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">Assets</h1>
              <p class="mt-2 text-gray-600">Manage your configuration items</p>
            </div>
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
    </div>

    <!-- Filters and Search -->
    <BaseCard>
      <div class="grid grid-cols-1 gap-4 md:grid-cols-6">
        <BaseInput
          v-model="searchQuery"
          placeholder="Search assets..."
          @input="handleSearch"
        >
          <template #prefix>
            <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
          </template>
        </BaseInput>
        
        <select
          v-model="selectedType"
          class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-constellation-500"
          @change="handleFilterChange"
        >
          <option value="">All Types</option>
          <!-- Infrastructure -->
          <option value="HARDWARE">Hardware</option>
          <option value="SOFTWARE">Software</option>
          <option value="NETWORK">Network</option>
          <!-- Applications and Services -->
          <option value="APPLICATION">Application</option>
          <option value="SERVICE">Service</option>
          <option value="ENDPOINT">Endpoint</option>
          <!-- Data and Content -->
          <option value="DATASET">Dataset</option>
          <option value="DATABASE">Database</option>
          <!-- Physical and Location -->
          <option value="LOCATION">Location</option>
          <option value="FACILITY">Facility</option>
          <!-- Security and Identity -->
          <option value="IDENTITY">Identity/Person</option>
          <option value="CREDENTIAL">Credential</option>
          <!-- Generic -->
          <option value="GENERIC">Generic</option>
        </select>

        <select
          v-model="selectedCriticality"
          class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-constellation-500"
          @change="handleFilterChange"
        >
          <option value="">All Criticality</option>
          <option value="CRITICAL">Critical</option>
          <option value="HIGH">High</option>
          <option value="MEDIUM">Medium</option>
          <option value="LOW">Low</option>
        </select>

        <select
          v-model="selectedEnvironment"
          class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-constellation-500"
          @change="handleFilterChange"
        >
          <option value="">All Environments</option>
          <option value="PROD">Production</option>
          <option value="STAGING">Staging</option>
          <option value="DEV">Development</option>
          <option value="TEST">Test</option>
        </select>

        <select
          v-model="selectedLifecycleState"
          class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-constellation-500"
          @change="handleFilterChange"
        >
          <option value="">All States</option>
          <option value="PLANNED">Planned</option>
          <option value="ACTIVE">Active</option>
          <option value="DEPRECATED">Deprecated</option>
          <option value="RETIRED">Retired</option>
        </select>

        <BaseButton variant="secondary" @click="clearFilters">
          Clear Filters
        </BaseButton>
        
        <BaseButton 
          v-if="allFilteredAssets.length > 0"
          :variant="isAllSelected ? 'danger' : 'success'" 
          size="sm"
          @click="isAllSelected ? clearSelection() : selectAll()"
        >
          <svg v-if="!isAllSelected" class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
          </svg>
          <svg v-else class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          {{ isAllSelected ? `Deselect All (${selectedAssets.size})` : `Select All (${allFilteredAssets.length})` }}
        </BaseButton>
      </div>
    </BaseCard>

    <!-- Bulk Actions Bar -->
    <div v-if="selectedAssets.size > 0" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <span class="text-sm font-medium text-blue-900">
            {{ selectedAssets.size }} asset(s) selected
          </span>
          <BaseButton variant="outline" size="sm" @click="clearSelection">
            Clear Selection
          </BaseButton>
        </div>
        
        <div class="flex items-center space-x-2">
          <select
            v-model="bulkLifecycleState"
            class="px-3 py-1 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Change Status</option>
            <option value="ACTIVE">Active</option>
            <option value="PLANNED">Planned</option>
            <option value="DEPRECATED">Deprecated</option>
            <option value="RETIRED">Retired</option>
          </select>
          
          <BaseButton
            variant="success"
            size="sm"
            :disabled="!bulkLifecycleState"
            @click="bulkUpdateStatus"
          >
            Update Status
          </BaseButton>
          
          <BaseButton
            variant="danger"
            size="sm"
            @click="confirmBulkDelete"
          >
            Delete Selected
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- Assets Grid -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-constellation-600"></div>
      <p class="mt-2 text-gray-600">Loading assets...</p>
    </div>

    <div v-else-if="filteredAssets.length === 0" class="text-center py-12">
      <ServerIcon class="mx-auto h-12 w-12 text-gray-400" />
      <p class="mt-2 text-gray-600">No assets found</p>
      <router-link 
        to="/assets/new" 
        class="mt-4 inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
      >
        Add your first asset
      </router-link>
    </div>

    <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <BaseCard
        v-for="asset in filteredAssets"
        :key="asset.id"
        shadow="md"
        hover
        :class="{ 'ring-2 ring-blue-500': selectedAssets.has(asset.id) }"
        @click="viewAsset(asset.id)"
      >
        <div class="space-y-4">
          <!-- Selection Checkbox -->
          <div class="flex items-center justify-start">
            <input
              type="checkbox"
              :checked="selectedAssets.has(asset.id)"
              @click.stop
              @change="toggleAssetSelection(asset.id, $event)"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
          </div>

          <!-- Asset Header -->
          <div class="flex items-center space-x-2">
            <component :is="getAssetIcon(asset.ci_type)" class="h-6 w-6 text-constellation-600" />
            <span class="text-sm font-medium text-gray-600">{{ asset.ci_type }}</span>
          </div>

          <!-- Asset Info -->
          <div>
            <h3 class="text-lg font-semibold text-gray-900">{{ asset.name }}</h3>
            <p class="text-sm text-gray-600 line-clamp-2">{{ asset.description }}</p>
          </div>

          <!-- Asset Metadata as List -->
          <div class="space-y-2">
            <!-- Criticality -->
            <div class="flex items-center space-x-2">
              <span class="text-xs text-gray-500">Criticality:</span>
              <span
                :class="[
                  'px-2 py-1 text-xs rounded-full',
                  getCriticalityClasses(asset.criticality)
                ]"
              >
                {{ asset.criticality }}
              </span>
            </div>
            
            <!-- Environment - uniquement pour les assets tangibles -->
            <div v-if="asset.category === 'tangible'" class="flex items-center space-x-2">
              <span class="text-xs text-gray-500">Environment:</span>
              <span class="text-xs font-medium text-gray-700">{{ asset.environment || 'N/A' }}</span>
            </div>
            
            <!-- Status - uniquement pour les assets tangibles -->
            <div v-if="asset.category === 'tangible'" class="flex items-center space-x-2">
              <span class="text-xs text-gray-500">Status:</span>
              <div class="flex items-center space-x-1">
                <div
                  :class="[
                    'h-2 w-2 rounded-full',
                    asset.lifecycle_state === 'ACTIVE' ? 'bg-green-500' :
                    asset.lifecycle_state === 'PLANNED' ? 'bg-blue-500' : 
                    asset.lifecycle_state === 'DECOMMISSIONED' ? 'bg-yellow-500' : 
                    asset.lifecycle_state === 'INACTIVE' ? 'bg-gray-500' : 'bg-gray-400'
                  ]"
                ></div>
                <span class="text-xs font-medium text-gray-700">{{ asset.lifecycle_state }}</span>
              </div>
            </div>
            
            <!-- Date -->
            <div class="flex items-center space-x-2">
              <span class="text-xs text-gray-500">Updated:</span>
              <span class="text-xs text-gray-600">{{ formatDate(asset.updated_at) }}</span>
            </div>
          </div>
        </div>
      </BaseCard>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex items-center justify-between">
      <p class="text-sm text-gray-700">
        Showing {{ (currentPage - 1) * pageSize + 1 }} to {{ Math.min(currentPage * pageSize, totalAssets) }} of {{ totalAssets }} results
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

  <!-- Delete Confirmation Modal -->
  <ConfirmDeleteModal
    :is-open="showDeleteModal"
    :title="deleteModalTitle"
    :message="deleteModalMessage"
    :details="deleteModalDetails"
    confirm-text="Delete"
    @confirm="handleConfirmDelete"
    @close="closeDeleteModal"
  />
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCMDBStore } from '@/stores/cmdb'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import ConfirmDeleteModal from '@/components/ConfirmDeleteModal.vue'
import {
  MagnifyingGlassIcon,
  ServerIcon,
  CpuChipIcon,
  CloudIcon,
  ComputerDesktopIcon,
  GlobeAltIcon,
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()
const cmdbStore = useCMDBStore()

// Initialize filters from query parameters
const loading = ref(false)
const searchQuery = ref(route.query.search as string || '')
const selectedType = ref(route.query.ci_type as string || route.query.type as string || '')
const selectedCriticality = ref(route.query.criticality as string || '')
const selectedEnvironment = ref(route.query.environment as string || '')
const selectedLifecycleState = ref(route.query.lifecycle_state as string || '')
const currentPage = ref(1)
const pageSize = ref(12)

// Bulk actions
const selectedAssets = ref(new Set<string>())
const bulkLifecycleState = ref('')

// Delete modal
const showDeleteModal = ref(false)
const deleteModalTitle = ref('')
const deleteModalMessage = ref('')
const deleteModalDetails = ref('')

// Computed properties
const allFilteredAssets = computed(() => {
  let assets = cmdbStore.cis

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    assets = assets.filter(asset => 
      asset.name.toLowerCase().includes(query) ||
      asset.description?.toLowerCase().includes(query) ||
      asset.ci_type.toLowerCase().includes(query)
    )
  }

  // Apply type filter
  if (selectedType.value) {
    assets = assets.filter(asset => asset.ci_type === selectedType.value)
  }

  // Apply criticality filter
  if (selectedCriticality.value) {
    assets = assets.filter(asset => asset.criticality === selectedCriticality.value)
  }

  // Apply environment filter
  if (selectedEnvironment.value) {
    assets = assets.filter(asset => asset.environment === selectedEnvironment.value)
  }

  // Apply lifecycle state filter
  if (selectedLifecycleState.value) {
    assets = assets.filter(asset => asset.lifecycle_state === selectedLifecycleState.value)
  }

  return assets
})

const filteredAssets = computed(() => {
  // Apply pagination to all filtered assets
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return allFilteredAssets.value.slice(start, end)
})

const totalAssets = computed(() => allFilteredAssets.value.length)
const totalPages = computed(() => Math.ceil(totalAssets.value / pageSize.value))

// Methods
const getAssetIcon = (type: string) => {
  const iconMap: Record<string, any> = {
    APPLICATION: ComputerDesktopIcon,
    DATABASE: ServerIcon,
    HARDWARE: CpuChipIcon,
    NETWORK: GlobeAltIcon,
    SERVICE: CloudIcon,
    STORAGE: ServerIcon,
    GENERIC: ServerIcon,
  }
  return iconMap[type] || ServerIcon
}

const getCriticalityClasses = (criticality: string) => {
  const classMap: Record<string, string> = {
    CRITICAL: 'bg-red-100 text-red-800',
    HIGH: 'bg-orange-100 text-orange-800',
    MEDIUM: 'bg-yellow-100 text-yellow-800',
    LOW: 'bg-green-100 text-green-800',
  }
  return classMap[criticality] || 'bg-gray-100 text-gray-800'
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const handleSearch = () => {
  currentPage.value = 1 // Reset to first page when searching
}

const handleFilterChange = () => {
  currentPage.value = 1 // Reset to first page when filtering
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedType.value = ''
  selectedCriticality.value = ''
  selectedEnvironment.value = ''
  selectedLifecycleState.value = ''
  currentPage.value = 1
}

const viewAsset = (id: string) => {
  router.push(`/assets/${id}`)
}

const loadAssets = async () => {
  loading.value = true
  try {
    await cmdbStore.fetchCIs()
  } catch (error) {
    console.error('Failed to load assets:', error)
  } finally {
    loading.value = false
  }
}

// Bulk actions functions
const toggleAssetSelection = (assetId: string, event: Event) => {
  const checkbox = event.target as HTMLInputElement
  if (checkbox.checked) {
    selectedAssets.value.add(assetId)
  } else {
    selectedAssets.value.delete(assetId)
  }
}

const clearSelection = () => {
  selectedAssets.value.clear()
  bulkLifecycleState.value = ''
}

const selectAll = () => {
  allFilteredAssets.value.forEach(asset => {
    selectedAssets.value.add(asset.id)
  })
}

const isAllSelected = computed(() => {
  return allFilteredAssets.value.length > 0 && 
         allFilteredAssets.value.every(asset => selectedAssets.value.has(asset.id))
})

const bulkUpdateStatus = async () => {
  if (!bulkLifecycleState.value || selectedAssets.value.size === 0) {
    return
  }

  const confirmation = confirm(
    `Are you sure you want to update ${selectedAssets.value.size} asset(s) to ${bulkLifecycleState.value}?`
  )

  if (!confirmation) return

  try {
    loading.value = true
    
    const selectedCount = selectedAssets.value.size
    
    // Update each selected asset
    const updatePromises = Array.from(selectedAssets.value).map((assetId: string) => {
      const asset = cmdbStore.cis.find(ci => ci.id === assetId)
      if (asset) {
        // Only send the minimal required fields plus the one we're changing
        const updateData = {
          name: asset.name,
          ci_type: asset.ci_type,
          lifecycle_state: bulkLifecycleState.value as 'ACTIVE' | 'INACTIVE' | 'PLANNED' | 'DECOMMISSIONED'
        }
        return cmdbStore.updateCI(assetId, updateData)
      }
      return Promise.resolve()
    })

    await Promise.all(updatePromises.filter(Boolean))
    
    // Refresh the list
    await cmdbStore.fetchCIs()
    
    // Clear selection
    clearSelection()
    
    alert(`Successfully updated ${selectedCount} asset(s)`)
  } catch (error: any) {
    console.error('Failed to bulk update assets:', error)
    console.error('Error response:', error.response?.data)
    
    let errorMessage = 'Failed to update assets. Please try again.'
    if (error.response?.data?.detail) {
      errorMessage = `Update failed: ${JSON.stringify(error.response.data.detail)}`
    } else if (error.message) {
      errorMessage = `Update failed: ${error.message}`
    }
    
    alert(errorMessage)
  } finally {
    loading.value = false
  }
}

const confirmBulkDelete = () => {
  if (selectedAssets.value.size === 0) return

  deleteModalTitle.value = 'Delete Assets'
  deleteModalMessage.value = `Are you sure you want to delete ${selectedAssets.value.size} asset(s)?`
  
  if (selectedAssets.value.size === allFilteredAssets.value.length && allFilteredAssets.value.length > 1) {
    deleteModalDetails.value = 'You are about to delete ALL visible assets. This action cannot be undone.'
  } else if (selectedAssets.value.size > 10) {
    deleteModalDetails.value = `You are deleting a large number of assets (${selectedAssets.value.size}). This action cannot be undone.`
  } else {
    deleteModalDetails.value = 'This action cannot be undone.'
  }
  
  showDeleteModal.value = true
}

const handleConfirmDelete = () => {
  showDeleteModal.value = false
  bulkDeleteAssets()
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
}

const bulkDeleteAssets = async () => {
  try {
    loading.value = true
    
    const selectedCount = selectedAssets.value.size
    
    // Delete each selected asset
    const deletePromises = Array.from(selectedAssets.value).map((assetId: string) => 
      cmdbStore.deleteCI(assetId)
    )

    await Promise.all(deletePromises)
    
    // Refresh the list
    await cmdbStore.fetchCIs()
    
    // Clear selection
    clearSelection()
    
    alert(`Successfully deleted ${selectedCount} asset(s)`)
  } catch (error: any) {
    console.error('Failed to bulk delete assets:', error)
    console.error('Error response:', error.response?.data)
    
    let errorMessage = 'Failed to delete assets. Please try again.'
    if (error.response?.data?.detail) {
      errorMessage = `Delete failed: ${JSON.stringify(error.response.data.detail)}`
    } else if (error.message) {
      errorMessage = `Delete failed: ${error.message}`
    }
    
    alert(errorMessage)
  } finally {
    loading.value = false
  }
}

// Watchers
watch([selectedType, selectedCriticality, selectedEnvironment, selectedLifecycleState], () => {
  currentPage.value = 1
})

// Lifecycle
onMounted(() => {
  loadAssets()
})
</script>