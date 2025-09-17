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
            <BaseButton @click="createNewAsset">
              <PlusIcon class="h-5 w-5 mr-2" />
              Add Asset
            </BaseButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <BaseCard>
      <div class="grid grid-cols-1 gap-4 md:grid-cols-4">
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
          <option value="Hardware">Hardware</option>
          <option value="Software">Software</option>
          <option value="Service">Service</option>
          <option value="Application">Application</option>
          <option value="Endpoint">Endpoint</option>
        </select>

        <select
          v-model="selectedCriticality"
          class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-constellation-500"
          @change="handleFilterChange"
        >
          <option value="">All Criticality</option>
          <option value="Critical">Critical</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>

        <BaseButton variant="secondary" @click="clearFilters">
          Clear Filters
        </BaseButton>
      </div>
    </BaseCard>

    <!-- Assets Grid -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-constellation-600"></div>
      <p class="mt-2 text-gray-600">Loading assets...</p>
    </div>

    <div v-else-if="filteredAssets.length === 0" class="text-center py-12">
      <ServerIcon class="mx-auto h-12 w-12 text-gray-400" />
      <p class="mt-2 text-gray-600">No assets found</p>
      <BaseButton class="mt-4" @click="createNewAsset">
        Add your first asset
      </BaseButton>
    </div>

    <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <BaseCard
        v-for="asset in filteredAssets"
        :key="asset.id"
        shadow="md"
        hover
        @click="viewAsset(asset.id)"
      >
        <div class="space-y-4">
          <!-- Asset Header -->
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
              <component :is="getAssetIcon(asset.ci_type)" class="h-6 w-6 text-constellation-600" />
              <span class="text-sm font-medium text-gray-600">{{ asset.ci_type }}</span>
            </div>
            <span
              :class="[
                'px-2 py-1 text-xs rounded-full',
                getCriticalityClasses(asset.criticality)
              ]"
            >
              {{ asset.criticality }}
            </span>
          </div>

          <!-- Asset Info -->
          <div>
            <h3 class="text-lg font-semibold text-gray-900">{{ asset.name }}</h3>
            <p class="text-sm text-gray-600 line-clamp-2">{{ asset.description }}</p>
          </div>

          <!-- Asset Metadata -->
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="text-gray-500">Environment:</span>
              <span class="ml-1 font-medium">{{ asset.environment || 'N/A' }}</span>
            </div>
            <div>
              <span class="text-gray-500">Status:</span>
              <span class="ml-1 font-medium">{{ asset.status || 'N/A' }}</span>
            </div>
          </div>

          <!-- Asset Status -->
          <div class="flex items-center justify-between pt-4 border-t border-gray-200">
            <div class="flex items-center space-x-2">
              <div
                :class="[
                  'h-2 w-2 rounded-full',
                  asset.status === 'Active' ? 'bg-green-500' :
                  asset.status === 'Inactive' ? 'bg-gray-500' : 'bg-red-500'
                ]"
              ></div>
              <span class="text-sm text-gray-600">{{ asset.status }}</span>
            </div>
            <span class="text-xs text-gray-500">
              {{ formatDate(asset.updated_at) }}
            </span>
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
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCMDBStore } from '@/stores/cmdb'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import {
  PlusIcon,
  MagnifyingGlassIcon,
  ServerIcon,
  CpuChipIcon,
  CloudIcon,
  ComputerDesktopIcon,
  GlobeAltIcon,
} from '@heroicons/vue/24/outline'

const router = useRouter()
const cmdbStore = useCMDBStore()

// Reactive data
const loading = ref(false)
const searchQuery = ref('')
const selectedType = ref('')
const selectedCriticality = ref('')
const currentPage = ref(1)
const pageSize = ref(12)

// Computed properties
const filteredAssets = computed(() => {
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

  // Apply pagination
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return assets.slice(start, end)
})

const totalAssets = computed(() => cmdbStore.cis.length)
const totalPages = computed(() => Math.ceil(totalAssets.value / pageSize.value))

// Methods
const getAssetIcon = (type: string) => {
  const iconMap: Record<string, any> = {
    Hardware: ServerIcon,
    Software: CpuChipIcon,
    Service: CloudIcon,
    Application: ComputerDesktopIcon,
    Endpoint: GlobeAltIcon,
  }
  return iconMap[type] || ServerIcon
}

const getCriticalityClasses = (criticality: string) => {
  const classMap: Record<string, string> = {
    Critical: 'bg-red-100 text-red-800',
    High: 'bg-orange-100 text-orange-800',
    Medium: 'bg-yellow-100 text-yellow-800',
    Low: 'bg-green-100 text-green-800',
  }
  return classMap[criticality] || 'bg-gray-100 text-gray-800'
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString()
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
  currentPage.value = 1
}

const createNewAsset = () => {
  router.push('/assets/new')
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

// Watchers
watch([selectedType, selectedCriticality], () => {
  currentPage.value = 1
})

// Lifecycle
onMounted(() => {
  loadAssets()
})
</script>