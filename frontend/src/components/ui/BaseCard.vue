<template>
  <div :class="cardClasses">
    <div v-if="$slots.header" class="px-4 py-5 sm:px-6 border-b border-gray-200">
      <slot name="header"></slot>
    </div>
    <div :class="bodyClasses">
      <slot></slot>
    </div>
    <div v-if="$slots.footer" class="px-4 py-4 sm:px-6 border-t border-gray-200 bg-gray-50">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  shadow?: 'none' | 'sm' | 'md' | 'lg'
  padding?: 'none' | 'sm' | 'md' | 'lg'
  hover?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  shadow: 'sm',
  padding: 'md',
  hover: false,
})

const cardClasses = computed(() => {
  const baseClasses = ['bg-white', 'rounded-lg', 'border', 'border-gray-200']

  // Shadow classes
  const shadowClasses = {
    none: [],
    sm: ['shadow-sm'],
    md: ['shadow-md'],
    lg: ['shadow-lg'],
  }

  const classes = [
    ...baseClasses,
    ...shadowClasses[props.shadow],
  ]

  if (props.hover) {
    classes.push('hover:shadow-md', 'transition-shadow', 'cursor-pointer')
  }

  return classes.join(' ')
})

const bodyClasses = computed(() => {
  const paddingClasses = {
    none: [],
    sm: ['px-3', 'py-3'],
    md: ['px-4', 'py-5', 'sm:px-6'],
    lg: ['px-6', 'py-6'],
  }

  return paddingClasses[props.padding].join(' ')
})
</script>