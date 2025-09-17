<template>
  <div class="space-y-1">
    <label
      v-if="label"
      :for="inputId"
      class="block text-sm font-medium text-gray-700"
    >
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <div class="relative">
      <div
        v-if="$slots.prefix"
        class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
      >
        <slot name="prefix"></slot>
      </div>
      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :class="inputClasses"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      />
      <div
        v-if="$slots.suffix"
        class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none"
      >
        <slot name="suffix"></slot>
      </div>
    </div>
    <p
      v-if="error"
      class="text-sm text-red-600"
    >
      {{ error }}
    </p>
    <p
      v-else-if="hint"
      class="text-sm text-gray-500"
    >
      {{ hint }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, useSlots } from 'vue'

interface Props {
  modelValue?: string | number
  type?: 'text' | 'email' | 'password' | 'number' | 'search' | 'url' | 'tel'
  label?: string
  placeholder?: string
  disabled?: boolean
  required?: boolean
  error?: string
  hint?: string
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false,
  required: false,
  size: 'md',
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  blur: [event: FocusEvent]
  focus: [event: FocusEvent]
}>()

const slots = useSlots()
const inputId = ref(`input-${Math.random().toString(36).substr(2, 9)}`)

const inputClasses = computed(() => {
  const baseClasses = [
    'block',
    'w-full',
    'border',
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
    sm: ['px-3', 'py-2', 'text-sm'],
    md: ['px-3', 'py-2', 'text-base'],
    lg: ['px-4', 'py-3', 'text-lg'],
  }

  // State classes
  const stateClasses = props.error
    ? [
        'border-red-300',
        'text-red-900',
        'placeholder-red-300',
        'focus:ring-red-500',
        'focus:border-red-500',
      ]
    : [
        'border-gray-300',
        'text-gray-900',
        'placeholder-gray-400',
        'focus:ring-constellation-500',
        'focus:border-constellation-500',
      ]

  const classes = [
    ...baseClasses,
    ...sizeClasses[props.size],
    ...stateClasses,
  ]

  // Add padding for prefix/suffix
  if (slots.prefix) {
    classes.push('pl-10')
  }
  if (slots.suffix) {
    classes.push('pr-10')
  }

  return classes.join(' ')
})

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}

const handleBlur = (event: FocusEvent) => {
  emit('blur', event)
}

const handleFocus = (event: FocusEvent) => {
  emit('focus', event)
}
</script>