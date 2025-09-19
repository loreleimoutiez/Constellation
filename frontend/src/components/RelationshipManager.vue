<template>
  <BaseCard>
    <template #header>
      <h2 class="text-lg font-semibold text-gray-900">Relationships</h2>
    </template>

    <!-- Existing Relationships -->
    <div v-if="relationships.length > 0" class="space-y-4 mb-6">
      <h3 class="text-md font-medium text-gray-700">Current Relationships</h3>
      <div class="space-y-2">
        <div 
          v-for="rel in relationships" 
          :key="rel.id"
          class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
        >
          <div class="flex items-center space-x-3">
            <component :is="getAssetIcon(rel.target.ci_type)" class="h-5 w-5 text-gray-600" />
            <div>
              <p class="font-medium text-gray-900">{{ rel.target.name }}</p>
              <p class="text-sm text-gray-500">{{ rel.relationship_type }}</p>
            </div>
          </div>
          <BaseButton 
            variant="danger" 
            size="sm"
            @click="removeRelationship(rel.id)"
          >
            Remove
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- Add New Relationship -->
    <div class="space-y-4">
      <h3 class="text-md font-medium text-gray-700">Add New Relationship</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Asset Selection -->
        <div>
          <label for="target_asset" class="block text-sm font-medium text-gray-700">Target Asset</label>
          <select
            id="target_asset"
            v-model="newRelationship.target_id"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
          >
            <option value="">Select asset...</option>
            <option 
              v-for="asset in availableAssets" 
              :key="asset.id" 
              :value="asset.id"
            >
              {{ asset.name }} ({{ asset.ci_type }})
            </option>
          </select>
        </div>

        <!-- Relationship Type -->
        <div>
          <label for="relationship_type" class="block text-sm font-medium text-gray-700">Relationship Type</label>
          <select
            id="relationship_type"
            v-model="newRelationship.relationship_type"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
          >
            <option value="">Select type...</option>
            <option value="DEPENDS_ON">Depends On</option>
            <option value="USES">Uses</option>
            <option value="HOSTS">Hosts</option>
            <option value="CONNECTS_TO">Connects To</option>
            <option value="RESPONSIBLE_FOR">Responsible For</option>
            <option value="APPLIES_TO">Applies To</option>
            <option value="GOVERNS">Governs</option>
            <option value="BELONGS_TO">Belongs To</option>
            <option value="RELATED_TO">Related To</option>
          </select>
        </div>

        <!-- Add Button -->
        <div class="flex items-end">
          <BaseButton
            :disabled="!canAddRelationship"
            @click="addRelationship"
            class="w-full"
          >
            Add Relationship
          </BaseButton>
        </div>
      </div>

      <!-- Description -->
      <div>
        <label for="description" class="block text-sm font-medium text-gray-700">Description (optional)</label>
        <textarea
          id="description"
          v-model="newRelationship.description"
          rows="2"
          placeholder="Describe this relationship..."
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-constellation-500 focus:border-constellation-500"
        ></textarea>
      </div>
    </div>
  </BaseCard>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useCMDBStore } from '@/stores/cmdb'
import type { CI } from '@/services/api'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import {
  ServerIcon,
  ComputerDesktopIcon,
  CpuChipIcon,
  CloudIcon,
  GlobeAltIcon,
} from '@heroicons/vue/24/outline'

// Props
interface Props {
  assetId?: string
  existingRelationships?: any[]
}

const props = withDefaults(defineProps<Props>(), {
  existingRelationships: () => []
})

// Emits
const emit = defineEmits<{
  relationshipAdded: [relationship: any]
  relationshipRemoved: [relationshipId: string]
}>()

// Store
const cmdbStore = useCMDBStore()

// Reactive data
const relationships = ref(props.existingRelationships)
const availableAssets = ref<CI[]>([])
const newRelationship = ref({
  target_id: '',
  relationship_type: '',
  description: ''
})

// Computed
const canAddRelationship = computed(() => {
  return !!(newRelationship.value.target_id && newRelationship.value.relationship_type)
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

const loadAvailableAssets = async () => {
  try {
    await cmdbStore.fetchCIs()
    // Filter out the current asset and already related assets
    availableAssets.value = cmdbStore.cis.filter(asset => {
      if (props.assetId && asset.id === props.assetId) return false
      return !relationships.value.some(rel => rel.target.id === asset.id)
    })
  } catch (error) {
    console.error('Failed to load available assets:', error)
  }
}

const addRelationship = async () => {
  if (!canAddRelationship.value || !props.assetId) return

  try {
    const relationshipData = {
      from_ci_id: props.assetId,
      to_ci_id: newRelationship.value.target_id,
      relationship_type: newRelationship.value.relationship_type,
      description: newRelationship.value.description || ''
    }

    // Call API to create relationship
    const response = await fetch('http://localhost:8000/api/v1/relationships', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(relationshipData)
    })

    if (!response.ok) {
      throw new Error('Failed to create relationship')
    }

    const createdRelationship = await response.json()
    
    // Find the target asset for display
    const targetAsset = availableAssets.value.find(a => a.id === newRelationship.value.target_id)
    
    if (targetAsset) {
      // Add to local relationships list
      relationships.value.push({
        id: createdRelationship.id || Date.now().toString(),
        relationship_type: newRelationship.value.relationship_type,
        target: targetAsset
      })

      // Remove from available assets
      availableAssets.value = availableAssets.value.filter(a => a.id !== newRelationship.value.target_id)

      // Emit event
      emit('relationshipAdded', createdRelationship)
    }

    // Reset form
    newRelationship.value = {
      target_id: '',
      relationship_type: '',
      description: ''
    }

  } catch (error) {
    console.error('Failed to add relationship:', error)
    alert('Failed to add relationship. Please try again.')
  }
}

const removeRelationship = async (relationshipId: string) => {
  if (!confirm('Are you sure you want to remove this relationship?')) return

  try {
    // Call API to delete relationship
    const response = await fetch(`http://localhost:8000/api/v1/relationships/${relationshipId}`, {
      method: 'DELETE'
    })

    if (!response.ok) {
      throw new Error('Failed to delete relationship')
    }

    // Remove from local list
    const removedRel = relationships.value.find(r => r.id === relationshipId)
    relationships.value = relationships.value.filter(r => r.id !== relationshipId)

    // Add back to available assets if we have the target
    if (removedRel) {
      const targetAsset = cmdbStore.cis.find(a => a.id === removedRel.target.id)
      if (targetAsset && !availableAssets.value.some(a => a.id === targetAsset.id)) {
        availableAssets.value.push(targetAsset)
      }
    }

    // Emit event
    emit('relationshipRemoved', relationshipId)

  } catch (error) {
    console.error('Failed to remove relationship:', error)
    alert('Failed to remove relationship. Please try again.')
  }
}

// Lifecycle
onMounted(() => {
  loadAvailableAssets()
})
</script>