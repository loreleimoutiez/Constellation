<template>
  <div class="relative">
    <label class="block text-sm font-medium text-gray-700 mb-2">
      Select Configuration Item for Analysis
    </label>
    
    <!-- Search Input -->
    <div class="relative">
      <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
      <input
        v-model="searchQuery"
        @input="handleSearch"
        @focus="showDropdown = true"
        @blur="handleBlur"
        type="text"
        placeholder="Search for a CI..."
        class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      />
    </div>

    <!-- Dropdown -->
    <div 
      v-if="showDropdown && (filteredCIs.length > 0 || isLoading)"
      class="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto"
    >
      <!-- Loading State -->
      <div v-if="isLoading" class="p-4 text-center text-gray-500">
        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500 mx-auto"></div>
        <p class="mt-2 text-sm">Loading CIs...</p>
      </div>

      <!-- CI List -->
      <div v-else-if="filteredCIs.length > 0">
        <button
          v-for="ci in filteredCIs"
          :key="ci.id"
          @mousedown="selectCI(ci)"
          class="w-full text-left px-4 py-3 hover:bg-gray-50 focus:bg-gray-50 focus:outline-none border-b border-gray-100 last:border-b-0"
        >
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <div class="font-medium text-gray-900">{{ ci.name }}</div>
              <div class="text-sm text-gray-500 flex items-center space-x-2">
                <span>{{ ci.ci_type }}</span>
                <span class="text-gray-300">•</span>
                <span :class="getCriticalityColor(ci.criticality)">
                  {{ ci.criticality }}
                </span>
                <span class="text-gray-300">•</span>
                <span>{{ ci.environment || 'N/A' }}</span>
              </div>
            </div>
            <div :class="getCriticalityBadgeColor(ci.criticality)" class="px-2 py-1 rounded-full text-xs font-medium">
              {{ ci.criticality }}
            </div>
          </div>
        </button>
      </div>

      <!-- No Results -->
      <div v-else class="p-4 text-center text-gray-500">
        <ExclamationCircleIcon class="h-8 w-8 mx-auto text-gray-400 mb-2" />
        <p class="text-sm">No CIs found matching "{{ searchQuery }}"</p>
      </div>
    </div>

    <!-- Selected CI Display -->
    <div v-if="selectedCI" class="mt-3 p-3 bg-blue-50 border border-blue-200 rounded-lg">
      <div class="flex items-center justify-between">
        <div>
          <div class="font-medium text-blue-900">{{ selectedCI.name }}</div>
          <div class="text-sm text-blue-700 flex items-center space-x-2">
            <span>{{ selectedCI.ci_type }}</span>
            <span class="text-blue-400">•</span>
            <span>{{ selectedCI.criticality }}</span>
            <span class="text-blue-400">•</span>
            <span>{{ selectedCI.environment || 'N/A' }}</span>
          </div>
        </div>
        <button
          @click="clearSelection"
          class="text-blue-600 hover:text-blue-800 p-1"
          title="Clear selection"
        >
          <XMarkIcon class="h-5 w-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { MagnifyingGlassIcon, ExclamationCircleIcon, XMarkIcon } from '@heroicons/vue/24/outline'
import type { CI } from '@/services/api'

interface Props {
  cis: CI[]
  isLoading?: boolean
  modelValue?: CI | null
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false,
  modelValue: null
})

const emit = defineEmits<{
  'update:modelValue': [ci: CI | null]
  'search': [query: string]
}>()

// State
const searchQuery = ref('')
const showDropdown = ref(false)
const selectedCI = ref<CI | null>(props.modelValue)

// Computed
const filteredCIs = computed(() => {
  if (!searchQuery.value) return props.cis.slice(0, 20) // Show first 20 by default
  
  const query = searchQuery.value.toLowerCase()
  return props.cis.filter(ci => 
    ci.name.toLowerCase().includes(query) ||
    ci.ci_type.toLowerCase().includes(query) ||
    ci.description?.toLowerCase().includes(query)
  ).slice(0, 20)
})

// Methods
const handleSearch = () => {
  showDropdown.value = true
  emit('search', searchQuery.value)
}

const handleBlur = () => {
  // Delay hiding dropdown to allow for click events
  setTimeout(() => {
    showDropdown.value = false
  }, 200)
}

const selectCI = (ci: CI) => {
  selectedCI.value = ci
  searchQuery.value = ci.name
  showDropdown.value = false
  emit('update:modelValue', ci)
}

const clearSelection = () => {
  selectedCI.value = null
  searchQuery.value = ''
  emit('update:modelValue', null)
}

const getCriticalityColor = (criticality: string) => {
  const colors = {
    'CRITICAL': 'text-red-600',
    'HIGH': 'text-orange-600',
    'MEDIUM': 'text-yellow-600',
    'LOW': 'text-green-600'
  }
  return colors[criticality as keyof typeof colors] || 'text-gray-600'
}

const getCriticalityBadgeColor = (criticality: string) => {
  const colors = {
    'CRITICAL': 'bg-red-100 text-red-800',
    'HIGH': 'bg-orange-100 text-orange-800',
    'MEDIUM': 'bg-yellow-100 text-yellow-800',
    'LOW': 'bg-green-100 text-green-800'
  }
  return colors[criticality as keyof typeof colors] || 'bg-gray-100 text-gray-800'
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  selectedCI.value = newValue
  searchQuery.value = newValue?.name || ''
})
</script>