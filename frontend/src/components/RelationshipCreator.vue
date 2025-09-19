<template>
  <div class="space-y-6">
    <div class="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-r-lg">
      <p class="text-sm text-blue-800 font-medium">
        Asset Relationships
      </p>
      <p class="text-xs text-blue-600 mt-1">
        Define relationships that will be created when this asset is saved.
      </p>
    </div>
    
    <div v-if="relationships.length === 0" class="text-center py-12 text-gray-500 bg-gray-50 rounded-lg border-2 border-dashed border-gray-200">
      <div class="space-y-2">
        <svg class="w-12 h-12 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
        </svg>
        <p class="font-medium">No relationships defined</p>
        <p class="text-sm">Click "Add Relationship" below to create one</p>
      </div>
    </div>
    
    <div v-else class="space-y-4">
      <h4 class="text-sm font-semibold text-gray-700 border-b border-gray-200 pb-2">
        Defined Relationships ({{ relationships.length }})
      </h4>
      <div 
        v-for="(relationship, index) in relationships" 
        :key="index"
        class="bg-white border border-gray-200 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1 space-y-2">
            <div class="flex items-center space-x-2">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {{ getRelationshipDisplay(relationship.relationship_type) }}
              </span>
            </div>
            <div class="text-sm text-gray-600">
              <strong>Target:</strong> {{ getTargetDisplayName(relationship.target_ci_id) }}
            </div>
            <div v-if="relationship.description" class="text-sm text-gray-600 bg-gray-50 p-2 rounded italic">
              "{{ relationship.description }}"
            </div>
          </div>
          <button
            @click="removeRelationship(index)"
            class="ml-4 text-red-500 hover:text-red-700 hover:bg-red-50 p-2 rounded-full transition-colors"
            title="Remove relationship"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
    
    <div class="border-t border-gray-200 pt-4">
      <button
        @click="showAddForm = !showAddForm"
        class="w-full py-3 px-4 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-blue-400 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200 font-medium"
      >
        <div class="flex items-center justify-center space-x-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
          <span>{{ showAddForm ? 'Cancel' : 'Add Relationship' }}</span>
        </div>
      </button>
    </div>
    
    <div v-if="showAddForm" class="bg-gray-50 border border-gray-200 rounded-lg p-6 space-y-6">
      <h4 class="text-lg font-semibold text-gray-800 border-b border-gray-300 pb-2">
        Add New Relationship
      </h4>
      
      <div class="space-y-6">
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700">
            Target Asset <span class="text-red-500">*</span>
          </label>
          <div class="relative">
            <input
              v-model="assetSearchQuery"
              @input="searchAssets"
              @focus="showAssetDropdown = true"
              type="text"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              placeholder="Search by asset name or enter ID directly"
            />
            <div 
              v-if="showAssetDropdown && (filteredAssets.length > 0 || isLoadingAssets)"
              class="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto"
            >
              <div v-if="isLoadingAssets" class="p-3 text-sm text-gray-500">
                Loading assets...
              </div>
              <div 
                v-for="asset in filteredAssets" 
                :key="asset.id"
                @click="selectAsset(asset)"
                class="p-3 hover:bg-gray-100 cursor-pointer border-b border-gray-100 last:border-b-0"
              >
                <div class="font-medium text-gray-900">{{ asset.name }}</div>
                <div class="text-sm text-gray-500">{{ asset.id }}</div>
                <div class="text-xs text-gray-400">{{ asset.ci_type }} • {{ asset.environment }}</div>
              </div>
              <div v-if="filteredAssets.length === 0 && !isLoadingAssets && assetSearchQuery" class="p-3 text-sm text-gray-500">
                No assets found. You can still enter an ID directly above.
              </div>
            </div>
          </div>
          <p class="text-xs text-gray-500">
            Start typing to search assets by name, or enter an asset ID directly
          </p>
        </div>
        
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700">
            Relationship Type <span class="text-red-500">*</span>
          </label>
          <select
            v-model="newRelationship.relationship_type"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          >
            <option value="">Select relationship type</option>
            <optgroup label="Technical Dependencies">
              <option value="DEPENDS_ON">Depends On</option>
              <option value="RUNS_ON">Runs On</option>
              <option value="HOSTS">Hosts</option>
              <option value="CONNECTS_TO">Connects To</option>
              <option value="INSTALLED_ON">Installed On</option>
              <option value="USES">Uses</option>
            </optgroup>
            <optgroup label="Data Relations">
              <option value="PRODUCES">Produces</option>
              <option value="CONSUMES">Consumes</option>
            </optgroup>
            <optgroup label="Generic">
              <option value="RELATED_TO">Related To</option>
            </optgroup>
          </select>
        </div>
      
        <div class="space-y-2">
          <label class="block text-sm font-semibold text-gray-700">
            Description <span class="text-gray-400">(Optional)</span>
          </label>
          <textarea
            v-model="newRelationship.description"
            rows="3"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors resize-none"
            placeholder="Describe this relationship and why it exists..."
          ></textarea>
        </div>
      </div>
      
      <div class="space-y-3 pt-4 border-t border-gray-300">
        <button
          @click="addRelationship"
          :disabled="!canAddRelationship"
          class="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-blue-600 transition-colors font-medium"
        >
          Add Relationship
        </button>
        <button
          @click="cancelAdd"
          class="w-full px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-medium"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useCMDBStore } from '@/stores/cmdb'
import type { CI } from '@/services/api'

interface RelationshipData {
  target_ci_id: string
  relationship_type: string
  description?: string
}

interface Props {
  modelValue: RelationshipData[]
  excludeCiId?: string | null
}

interface Emits {
  (e: 'update:modelValue', value: RelationshipData[]): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
const cmdbStore = useCMDBStore()

const showAddForm = ref(false)
const showAssetDropdown = ref(false)
const assetSearchQuery = ref('')
const isLoadingAssets = ref(false)
const availableAssets = ref<CI[]>([])

const newRelationship = ref<RelationshipData>({
  target_ci_id: '',
  relationship_type: '',
  description: ''
})

const relationships = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const filteredAssets = computed(() => {
  if (!assetSearchQuery.value.trim()) return availableAssets.value.slice(0, 10)
  
  const query = assetSearchQuery.value.toLowerCase()
  return availableAssets.value.filter(asset => 
    asset.name.toLowerCase().includes(query) ||
    asset.id.toLowerCase().includes(query) ||
    asset.ci_type.toLowerCase().includes(query)
  ).slice(0, 10)
})

const canAddRelationship = computed(() => {
  return newRelationship.value.target_ci_id.trim() && 
         newRelationship.value.relationship_type &&
         newRelationship.value.target_ci_id !== props.excludeCiId
})

const getRelationshipDisplay = (type: string) => {
  const typeMap: Record<string, string> = {
    'DEPENDS_ON': 'Depends On',
    'RUNS_ON': 'Runs On',
    'HOSTS': 'Hosts',
    'CONNECTS_TO': 'Connects To',
    'INSTALLED_ON': 'Installed On',
    'USES': 'Uses',
    'PRODUCES': 'Produces',
    'CONSUMES': 'Consumes',
    'RELATED_TO': 'Related To'
  }
  return typeMap[type] || type
}

const getTargetDisplayName = (targetId: string) => {
  const asset = availableAssets.value.find(asset => asset.id === targetId)
  return asset ? `${asset.name} (${targetId.slice(0, 8)}...)` : targetId
}

const loadAssets = async () => {
  if (availableAssets.value.length > 0) return
  
  isLoadingAssets.value = true
  try {
    await cmdbStore.fetchCIs({ limit: 100 })
    availableAssets.value = cmdbStore.cis || []
  } catch (error) {
    console.error('Failed to load assets:', error)
  } finally {
    isLoadingAssets.value = false
  }
}

const searchAssets = async () => {
  // Load assets if not already loaded
  if (availableAssets.value.length === 0) {
    await loadAssets()
  }
}

const selectAsset = (asset: CI) => {
  newRelationship.value.target_ci_id = asset.id
  assetSearchQuery.value = `${asset.name} (${asset.id.slice(0, 8)}...)`
  showAssetDropdown.value = false
}

const addRelationship = () => {
  if (canAddRelationship.value) {
    const newRels = [...relationships.value, { ...newRelationship.value }]
    relationships.value = newRels
    cancelAdd()
  }
}

const removeRelationship = (index: number) => {
  const newRels = relationships.value.filter((_, i) => i !== index)
  relationships.value = newRels
}

const cancelAdd = () => {
  showAddForm.value = false
  showAssetDropdown.value = false
  assetSearchQuery.value = ''
  newRelationship.value = {
    target_ci_id: '',
    relationship_type: '',
    description: ''
  }
}

// Close dropdown when clicking outside
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement
  if (!target.closest('.relative')) {
    showAssetDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  return () => {
    document.removeEventListener('click', handleClickOutside)
  }
})
</script>