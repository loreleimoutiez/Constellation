<template>
  <div class="space-y-6">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-constellation-600"></div>
      <p class="mt-2 text-gray-600">Loading asset...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-600 mb-4">⚠️ Error loading asset</div>
      <p class="text-gray-600">{{ error }}</p>
      <BaseButton class="mt-4" @click="$router.push('/assets')">
        Back to Assets
      </BaseButton>
    </div>

    <!-- Asset Details -->
    <template v-else-if="asset">
      <!-- Page Header -->
      <div class="bg-white shadow">
        <div class="px-4 sm:px-6 lg:px-8">
          <div class="py-6">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <BaseButton variant="secondary" @click="$router.push('/assets')">
                  ← Back
                </BaseButton>
                <div>
                  <div class="flex items-center space-x-3">
                    <component :is="getAssetIcon(asset.ci_type)" class="h-8 w-8 text-constellation-600" />
                    <h1 class="text-3xl font-bold text-gray-900">{{ asset.name }}</h1>
                    <span
                      :class="[
                        'px-3 py-1 text-sm rounded-full',
                        getCriticalityClasses(asset.criticality)
                      ]"
                    >
                      {{ asset.criticality }}
                    </span>
                  </div>
                  <p class="mt-2 text-gray-600">{{ asset.description || 'No description available' }}</p>
                </div>
              </div>
              <div class="flex space-x-3">
                <BaseButton variant="secondary" @click="editAsset">
                  <PencilIcon class="h-5 w-5 mr-2" />
                  Edit
                </BaseButton>
                <BaseButton variant="danger" @click="deleteAsset">
                  <TrashIcon class="h-5 w-5 mr-2" />
                  Delete
                </BaseButton>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Asset Information Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Basic Information -->
        <div class="lg:col-span-2 space-y-6">
          <!-- General Info -->
          <BaseCard>
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">General Information</h2>
            </template>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700">Asset Type</label>
                <p class="mt-1 text-sm text-gray-900">{{ asset.ci_type }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Criticality</label>
                <p class="mt-1 text-sm text-gray-900">{{ asset.criticality }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Environment</label>
                <p class="mt-1 text-sm text-gray-900">{{ asset.environment }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Lifecycle State</label>
                <div class="flex items-center space-x-2 mt-1">
                  <div
                    :class="[
                      'h-2 w-2 rounded-full',
                      asset.lifecycle_state === 'ACTIVE' ? 'bg-green-500' :
                      asset.lifecycle_state === 'PLANNED' ? 'bg-blue-500' : 
                      asset.lifecycle_state === 'DEPRECATED' ? 'bg-yellow-500' : 'bg-gray-500'
                    ]"
                  ></div>
                  <span class="text-sm text-gray-900">{{ asset.lifecycle_state }}</span>
                </div>
              </div>
            </div>
          </BaseCard>

          <!-- Technical Details -->
          <BaseCard v-if="hasTechnicalDetails">
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Technical Details</h2>
            </template>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div v-if="asset.hostname">
                <label class="block text-sm font-medium text-gray-700">Hostname</label>
                <p class="mt-1 text-sm text-gray-900">{{ asset.hostname }}</p>
              </div>
              <div v-if="asset.ip_address">
                <label class="block text-sm font-medium text-gray-700">IP Address</label>
                <p class="mt-1 text-sm text-gray-900">{{ asset.ip_address }}</p>
              </div>
              <div v-if="asset.fqdn">
                <label class="block text-sm font-medium text-gray-700">FQDN</label>
                <p class="mt-1 text-sm text-gray-900">{{ asset.fqdn }}</p>
              </div>
              <div v-if="asset.vendor">
                <label class="block text-sm font-medium text-gray-700">Vendor</label>
                <p class="mt-1 text-sm text-gray-900">{{ asset.vendor }}</p>
              </div>
              <div v-if="asset.model">
                <label class="block text-sm font-medium text-gray-700">Model</label>
                <p class="mt-1 text-sm text-gray-900">{{ asset.model }}</p>
              </div>
              <div v-if="asset.location">
                <label class="block text-sm font-medium text-gray-700">Location</label>
                <p class="mt-1 text-sm text-gray-900">{{ asset.location }}</p>
              </div>
            </div>
          </BaseCard>

          <!-- Operational Flags -->
          <BaseCard>
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Operational Status</h2>
            </template>
            
            <div class="grid grid-cols-2 gap-6">
              <div class="flex items-center space-x-2">
                <div :class="[
                  'h-3 w-3 rounded-full',
                  asset.monitoring_enabled ? 'bg-green-500' : 'bg-gray-300'
                ]"></div>
                <span class="text-sm text-gray-900">Monitoring {{ asset.monitoring_enabled ? 'Enabled' : 'Disabled' }}</span>
              </div>
              <div class="flex items-center space-x-2">
                <div :class="[
                  'h-3 w-3 rounded-full',
                  asset.backup_enabled ? 'bg-green-500' : 'bg-gray-300'
                ]"></div>
                <span class="text-sm text-gray-900">Backup {{ asset.backup_enabled ? 'Enabled' : 'Disabled' }}</span>
              </div>
            </div>
          </BaseCard>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Quick Actions -->
          <BaseCard>
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Quick Actions</h2>
            </template>
            
            <div class="space-y-3">
              <BaseButton variant="secondary" size="sm" class="w-full" @click="viewRelationships">
                <ShareIcon class="h-4 w-4 mr-2" />
                View Relationships
              </BaseButton>
              <BaseButton variant="secondary" size="sm" class="w-full" @click="runImpactAnalysis">
                <ChartBarIcon class="h-4 w-4 mr-2" />
                Impact Analysis
              </BaseButton>
              <BaseButton variant="secondary" size="sm" class="w-full" @click="editAsset">
                <PencilIcon class="h-4 w-4 mr-2" />
                Edit Asset
              </BaseButton>
            </div>
          </BaseCard>

          <!-- Metadata -->
          <BaseCard>
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Metadata</h2>
            </template>
            
            <div class="space-y-4 text-sm">
              <div>
                <label class="block font-medium text-gray-700">Asset ID</label>
                <p class="mt-1 text-gray-900 font-mono text-xs">{{ asset.id }}</p>
              </div>
              <div>
                <label class="block font-medium text-gray-700">Created</label>
                <p class="mt-1 text-gray-900">{{ formatDate(asset.created_at) }}</p>
              </div>
              <div>
                <label class="block font-medium text-gray-700">Last Updated</label>
                <p class="mt-1 text-gray-900">{{ formatDate(asset.updated_at) }}</p>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCMDBStore } from '@/stores/cmdb'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import {
  ServerIcon,
  PencilIcon,
  TrashIcon,
  ShareIcon,
  ChartBarIcon,
  ComputerDesktopIcon,
  CpuChipIcon,
  CloudIcon,
  GlobeAltIcon,
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()
const cmdbStore = useCMDBStore()

// Reactive data
const loading = ref(false)
const error = ref<string | null>(null)
const asset = ref(null)

// Computed
const hasTechnicalDetails = computed(() => {
  if (!asset.value) return false
  return !!(
    asset.value.hostname ||
    asset.value.ip_address ||
    asset.value.fqdn ||
    asset.value.vendor ||
    asset.value.model ||
    asset.value.location
  )
})

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
  if (!date) return 'Unknown'
  try {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return 'Invalid date'
  }
}

const loadAsset = async () => {
  const assetId = route.params.id as string
  if (!assetId) {
    error.value = 'No asset ID provided'
    return
  }

  loading.value = true
  error.value = null

  try {
    // Try to get from store first
    await cmdbStore.fetchCIs()
    const foundAsset = cmdbStore.cis.find(ci => ci.id === assetId)
    
    if (foundAsset) {
      asset.value = foundAsset
    } else {
      // If not in store, try to fetch individually
      const fetchedAsset = await cmdbStore.fetchCI(assetId)
      asset.value = fetchedAsset
    }
  } catch (err) {
    console.error('Failed to load asset:', err)
    error.value = err instanceof Error ? err.message : 'Failed to load asset'
  } finally {
    loading.value = false
  }
}

const editAsset = () => {
  if (asset.value) {
    // For now, just show a placeholder
    alert('Edit functionality will be implemented in the next step!')
    // router.push(`/assets/${asset.value.id}/edit`)
  }
}

const deleteAsset = () => {
  if (asset.value && confirm(`Are you sure you want to delete "${asset.value.name}"?`)) {
    // For now, just show a placeholder
    alert('Delete functionality will be implemented in the next step!')
    // Implement delete logic here
  }
}

const viewRelationships = () => {
  alert('Relationships view will be implemented in Phase 4!')
}

const runImpactAnalysis = () => {
  alert('Impact analysis will be implemented in Phase 4!')
}

// Lifecycle
onMounted(() => {
  loadAsset()
})
</script>