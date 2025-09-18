<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="bg-white shadow">
      <div class="px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">
                {{ isEditing ? 'Edit Asset' : 'Create Asset' }}
              </h1>
              <p class="mt-2 text-gray-600">
                {{ isEditing ? 'Update asset information' : 'Add a new configuration item to your CMDB' }}
              </p>
            </div>
            <BaseButton variant="secondary" @click="$router.push('/assets')">
              Cancel
            </BaseButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Form -->
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Main Form -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Basic Information -->
          <BaseCard>
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Basic Information</h2>
            </template>
            
            <div class="space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="name" class="block text-sm font-medium text-gray-700">Name *</label>
                  <BaseInput
                    id="name"
                    v-model="form.name"
                    placeholder="Enter asset name"
                    required
                    :error="errors.name"
                  />
                </div>
                
                <div>
                  <label for="ci_type" class="block text-sm font-medium text-gray-700">Type *</label>
                  <select
                    id="ci_type"
                    v-model="form.ci_type"
                    required
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
                    :class="{ 'border-red-500': errors.ci_type }"
                  >
                    <option value="">Select type</option>
                    <option value="APPLICATION">Application</option>
                    <option value="DATABASE">Database</option>
                    <option value="HARDWARE">Hardware</option>
                    <option value="NETWORK">Network</option>
                    <option value="SERVICE">Service</option>
                    <option value="STORAGE">Storage</option>
                    <option value="GENERIC">Generic</option>
                  </select>
                  <p v-if="errors.ci_type" class="mt-1 text-sm text-red-600">{{ errors.ci_type }}</p>
                </div>
              </div>

              <div>
                <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
                <textarea
                  id="description"
                  v-model="form.description"
                  rows="3"
                  placeholder="Describe this asset..."
                  class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
                ></textarea>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label for="criticality" class="block text-sm font-medium text-gray-700">Criticality *</label>
                  <select
                    id="criticality"
                    v-model="form.criticality"
                    required
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
                  >
                    <option value="LOW">Low</option>
                    <option value="MEDIUM">Medium</option>
                    <option value="HIGH">High</option>
                    <option value="CRITICAL">Critical</option>
                  </select>
                </div>

                <div>
                  <label for="environment" class="block text-sm font-medium text-gray-700">Environment *</label>
                  <select
                    id="environment"
                    v-model="form.environment"
                    required
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
                  >
                    <option value="DEV">Development</option>
                    <option value="TEST">Test</option>
                    <option value="STAGING">Staging</option>
                    <option value="PROD">Production</option>
                  </select>
                </div>

                <div>
                  <label for="lifecycle_state" class="block text-sm font-medium text-gray-700">Lifecycle State</label>
                  <select
                    id="lifecycle_state"
                    v-model="form.lifecycle_state"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
                  >
                    <option value="PLANNED">Planned</option>
                    <option value="ACTIVE">Active</option>
                    <option value="DEPRECATED">Deprecated</option>
                    <option value="RETIRED">Retired</option>
                  </select>
                </div>
              </div>
            </div>
          </BaseCard>

          <!-- Technical Information -->
          <BaseCard>
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Technical Information</h2>
            </template>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label for="hostname" class="block text-sm font-medium text-gray-700">Hostname</label>
                <BaseInput
                  id="hostname"
                  v-model="form.hostname"
                  placeholder="server01.domain.com"
                />
              </div>

              <div>
                <label for="ip_address" class="block text-sm font-medium text-gray-700">IP Address</label>
                <BaseInput
                  id="ip_address"
                  v-model="form.ip_address"
                  placeholder="192.168.1.100"
                />
              </div>

              <div>
                <label for="fqdn" class="block text-sm font-medium text-gray-700">FQDN</label>
                <BaseInput
                  id="fqdn"
                  v-model="form.fqdn"
                  placeholder="server01.production.company.com"
                />
              </div>

              <div>
                <label for="vendor" class="block text-sm font-medium text-gray-700">Vendor</label>
                <BaseInput
                  id="vendor"
                  v-model="form.vendor"
                  placeholder="Dell, HP, Cisco..."
                />
              </div>

              <div>
                <label for="model" class="block text-sm font-medium text-gray-700">Model</label>
                <BaseInput
                  id="model"
                  v-model="form.model"
                  placeholder="PowerEdge R750, ProLiant DL380..."
                />
              </div>

              <div>
                <label for="location" class="block text-sm font-medium text-gray-700">Location</label>
                <BaseInput
                  id="location"
                  v-model="form.location"
                  placeholder="DataCenter-A-Rack-05"
                />
              </div>
            </div>
          </BaseCard>

          <!-- Operational Flags -->
          <BaseCard>
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Operational Settings</h2>
            </template>
            
            <div class="space-y-4">
              <div class="flex items-center">
                <input
                  id="monitoring_enabled"
                  v-model="form.monitoring_enabled"
                  type="checkbox"
                  class="h-4 w-4 text-constellation-600 focus:ring-constellation-500 border-gray-300 rounded"
                />
                <label for="monitoring_enabled" class="ml-2 block text-sm text-gray-900">
                  Enable monitoring for this asset
                </label>
              </div>

              <div class="flex items-center">
                <input
                  id="backup_enabled"
                  v-model="form.backup_enabled"
                  type="checkbox"
                  class="h-4 w-4 text-constellation-600 focus:ring-constellation-500 border-gray-300 rounded"
                />
                <label for="backup_enabled" class="ml-2 block text-sm text-gray-900">
                  Enable backup for this asset
                </label>
              </div>
            </div>
          </BaseCard>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Preview -->
          <BaseCard>
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Preview</h2>
            </template>
            
            <div class="space-y-4">
              <div class="flex items-center space-x-3">
                <component :is="getAssetIcon(form.ci_type)" class="h-6 w-6 text-constellation-600" />
                <div>
                  <p class="font-medium text-gray-900">{{ form.name || 'Asset Name' }}</p>
                  <p class="text-sm text-gray-500">{{ form.ci_type || 'TYPE' }}</p>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Criticality:</span>
                <span
                  :class="[
                    'px-2 py-1 text-xs rounded-full',
                    getCriticalityClasses(form.criticality)
                  ]"
                >
                  {{ form.criticality || 'MEDIUM' }}
                </span>
              </div>

              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">Environment:</span>
                <span class="text-sm font-medium">{{ form.environment || 'PROD' }}</span>
              </div>

              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">State:</span>
                <div class="flex items-center space-x-2">
                  <div
                    :class="[
                      'h-2 w-2 rounded-full',
                      form.lifecycle_state === 'ACTIVE' ? 'bg-green-500' :
                      form.lifecycle_state === 'PLANNED' ? 'bg-blue-500' : 
                      form.lifecycle_state === 'DEPRECATED' ? 'bg-yellow-500' : 'bg-gray-500'
                    ]"
                  ></div>
                  <span class="text-sm">{{ form.lifecycle_state || 'ACTIVE' }}</span>
                </div>
              </div>
            </div>
          </BaseCard>

          <!-- Actions -->
          <BaseCard>
            <template #header>
              <h2 class="text-lg font-semibold text-gray-900">Actions</h2>
            </template>
            
            <div class="space-y-3">
              <BaseButton
                type="submit"
                :variant="buttonVariant"
                :loading="loading"
                :disabled="!isFormValid"
                class="w-full"
              >
                {{ buttonText }}
              </BaseButton>
              
              <BaseButton
                variant="secondary"
                type="button"
                class="w-full"
                @click="resetForm"
              >
                Reset Form
              </BaseButton>

              <BaseButton
                variant="outline"
                type="button"
                class="w-full"
                @click="$router.push('/assets')"
              >
                Cancel
              </BaseButton>
            </div>
          </BaseCard>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCMDBStore } from '@/stores/cmdb'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import {
  ServerIcon,
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
const errors = ref<Record<string, string>>({})

// Check if we're in edit mode
const isEditing = computed(() => route.params.id !== undefined)

// Form data
const form = ref({
  name: '',
  description: '',
  ci_type: '',
  criticality: 'MEDIUM',
  environment: 'PROD',
  lifecycle_state: 'ACTIVE',
  hostname: '',
  ip_address: '',
  fqdn: '',
  vendor: '',
  model: '',
  location: '',
  monitoring_enabled: true,
  backup_enabled: false,
})

// Computed
const isFormValid = computed(() => {
  return !!(form.value.name.trim() && form.value.ci_type && form.value.criticality && form.value.environment)
})

const buttonText = computed(() => {
  if (loading.value) {
    return isEditing.value ? 'Updating...' : 'Creating...'
  }
  return isEditing.value ? 'Update Asset' : 'Create Asset'
})

const buttonVariant = computed(() => {
  if (loading.value) return 'secondary'
  return isFormValid.value ? 'success' : 'secondary'
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

const validateForm = () => {
  errors.value = {}

  if (!form.value.name.trim()) {
    errors.value.name = 'Name is required'
  }

  if (!form.value.ci_type) {
    errors.value.ci_type = 'Type is required'
  }

  return Object.keys(errors.value).length === 0
}

const resetForm = () => {
  form.value = {
    name: '',
    description: '',
    ci_type: '',
    criticality: 'MEDIUM',
    environment: 'PROD',
    lifecycle_state: 'ACTIVE',
    hostname: '',
    ip_address: '',
    fqdn: '',
    vendor: '',
    model: '',
    location: '',
    monitoring_enabled: true,
    backup_enabled: false,
  }
  errors.value = {}
}

const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  loading.value = true

  try {
    // Clean up empty strings and prepare data
    const cleanedForm = Object.fromEntries(
      Object.entries(form.value).filter(([_, value]) => value !== '' && value !== null)
    )

    if (isEditing.value) {
      // Update existing asset
      await cmdbStore.updateCI(route.params.id as string, cleanedForm)
    } else {
      // Create new asset
      await cmdbStore.createCI(cleanedForm)
    }

    // Redirect to assets list
    router.push('/assets')
  } catch (error) {
    // Show user-friendly error message
    let errorMessage = 'Failed to save asset. Please try again.'
    if (error.response?.data?.detail) {
      errorMessage = `Validation error: ${JSON.stringify(error.response.data.detail)}`
    }
    
    alert(errorMessage)
  } finally {
    loading.value = false
  }
}

const loadAssetForEditing = async () => {
  if (!isEditing.value) return

  const assetId = route.params.id as string
  loading.value = true

  try {
    await cmdbStore.fetchCIs()
    const asset = cmdbStore.cis.find(ci => ci.id === assetId)
    
    if (asset) {
      // Populate form with existing asset data
      form.value = {
        name: asset.name || '',
        description: asset.description || '',
        ci_type: asset.ci_type || '',
        criticality: asset.criticality || 'MEDIUM',
        environment: asset.environment || 'PROD',
        lifecycle_state: asset.lifecycle_state || 'ACTIVE',
        hostname: asset.hostname || '',
        ip_address: asset.ip_address || '',
        fqdn: asset.fqdn || '',
        vendor: asset.vendor || '',
        model: asset.model || '',
        location: asset.location || '',
        monitoring_enabled: asset.monitoring_enabled ?? true,
        backup_enabled: asset.backup_enabled ?? false,
      }
    } else {
      // Asset not found
      router.push('/assets')
    }
  } catch (error) {
    console.error('Failed to load asset for editing:', error)
    router.push('/assets')
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  if (isEditing.value) {
    loadAssetForEditing()
  }
})
</script>