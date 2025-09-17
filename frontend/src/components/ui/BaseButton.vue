<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <svg
      v-if="loading"
      class="animate-spin -ml-1 mr-3 h-5 w-5"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      ></circle>
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'outline'
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  disabled?: boolean
  loading?: boolean
  fullWidth?: boolean
  type?: 'button' | 'submit' | 'reset'
}

const props = withDefaults(defineProps<ButtonProps>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
  loading: false,
  fullWidth: false,
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const buttonClasses = computed(() => {
  const baseClasses = [
    'inline-flex',
    'items-center',
    'justify-center',
    'font-medium',
    'rounded-md',
    'transition-colors',
    'focus:outline-none',
    'focus:ring-2',
    'focus:ring-offset-2',
    'disabled:opacity-50',
    'disabled:cursor-not-allowed',
  ]

  // Size classes
const sizeClasses = {
  xs: ['px-2.5', 'py-1.5', 'text-xs'],
  sm: ['px-3', 'py-2', 'text-sm'],
  md: ['px-4', 'py-2', 'text-sm'],
  lg: ['px-4', 'py-2', 'text-base'],
  xl: ['px-6', 'py-3', 'text-base'],
}  // Variant classes
const variantClasses = {
  primary: [
    'bg-constellation-600',
    'text-white',
    'hover:bg-constellation-700',
    'focus:ring-constellation-500',
    'border-transparent',
  ],
  secondary: [
    'bg-gray-600',
    'text-white',
    'hover:bg-gray-700',
    'focus:ring-gray-500',
    'border-transparent',
  ],
  success: [
    'bg-green-600',
    'text-white',
    'hover:bg-green-700',
    'focus:ring-green-500',
    'border-transparent',
  ],
  danger: [
    'bg-red-600',
    'text-white',
    'hover:bg-red-700',
    'focus:ring-red-500',
    'border-transparent',
  ],
  warning: [
    'bg-yellow-600',
    'text-white',
    'hover:bg-yellow-700',
    'focus:ring-yellow-500',
    'border-transparent',
  ],
  info: [
    'bg-blue-600',
    'text-white',
    'hover:bg-blue-700',
    'focus:ring-blue-500',
    'border-transparent',
  ],
  outline: [
    'bg-transparent',
    'text-gray-700',
    'border-gray-300',
    'hover:bg-gray-50',
    'focus:ring-gray-500',
  ],
}

const classes = [
    ...baseClasses,
    ...sizeClasses[props.size],
    ...variantClasses[props.variant],
  ]

  if (props.fullWidth) {
    classes.push('w-full')
  }

  return classes.join(' ')
})

const handleClick = (event: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>