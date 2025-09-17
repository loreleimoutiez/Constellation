<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="bg-white shadow">
      <div class="px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-bold text-gray-900">Asset Details</h1>
              <p class="mt-2 text-gray-600">View and edit asset information</p>
            </div>
            <BaseButton @click="editAsset">
              <PencilIcon class="h-5 w-5 mr-2" />
              Edit
            </BaseButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Asset Details -->
    <BaseCard shadow="md">
      <div class="text-center py-12">
        <ServerIcon class="mx-auto h-12 w-12 text-gray-400" />
        <p class="mt-2 text-gray-600">Asset detail view coming soon</p>
        <p class="text-sm text-gray-500">ID: {{ $route.params.id }}</p>
      </div>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { ServerIcon, PencilIcon } from '@heroicons/vue/24/outline'

const router = useRouter()

const editAsset = () => {
  console.log('Edit asset functionality coming soon')
}
</script>