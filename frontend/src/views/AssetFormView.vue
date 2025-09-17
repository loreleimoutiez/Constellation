<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="bg-white shadow">
      <div class="px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">Create Asset</h1>
              <p class="mt-2 text-gray-600">Add a new configuration item</p>
            </div>
            <BaseButton variant="secondary" @click="$router.push('/assets')">
              Cancel
            </BaseButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Asset Form -->
    <BaseCard shadow="md">
      <div class="text-center py-12">
        <PlusIcon class="mx-auto h-12 w-12 text-gray-400" />
        <p class="mt-2 text-gray-600">Asset creation form coming soon</p>
        <p class="text-sm text-gray-500">Will integrate with CMDB API</p>
      </div>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { PlusIcon } from '@heroicons/vue/24/outline'
</script>