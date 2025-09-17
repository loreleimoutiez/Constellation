<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="bg-white shadow">
      <div class="px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <h1 class="text-3xl font-bold text-gray-900">Impact Analysis</h1>
          <p class="mt-2 text-gray-600">Analyze the impact of changes and failures</p>
        </div>
      </div>
    </div>

    <!-- Analysis Tools -->
    <BaseCard shadow="md">
      <div class="text-center py-12">
        <ExclamationTriangleIcon class="mx-auto h-12 w-12 text-gray-400" />
        <p class="mt-2 text-gray-600">Impact analysis tools coming soon</p>
        <p class="text-sm text-gray-500">Will connect to backend impact endpoints</p>
      </div>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'
</script>