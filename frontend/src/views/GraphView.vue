<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="bg-white shadow">
      <div class="px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <h1 class="text-3xl font-bold text-gray-900">Relationship Graph</h1>
          <p class="mt-2 text-gray-600">Visualize your infrastructure dependencies</p>
        </div>
      </div>
    </div>

    <!-- Graph Container -->
    <BaseCard shadow="md" padding="none">
      <div class="h-96 bg-gray-50 flex items-center justify-center">
        <div class="text-center">
          <ChartBarIcon class="mx-auto h-12 w-12 text-gray-400" />
          <p class="mt-2 text-gray-600">Graph visualization coming soon</p>
          <p class="text-sm text-gray-500">Will use vis-network or d3.js</p>
        </div>
      </div>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import { ChartBarIcon } from '@heroicons/vue/24/outline'
</script>