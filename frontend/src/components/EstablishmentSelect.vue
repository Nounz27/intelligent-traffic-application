<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },

  items: {
    type: Array,
    default: () => []
  },

  label: {
    type: String,
    required: true
  },

  placeholder: {
    type: String,
    default: 'Seleccionar establecimiento'
  },

  kind: {
    type: String,
    default: 'all'
  }
})

const emit = defineEmits(['update:modelValue'])

const filteredItems = computed(() => {
  if (props.kind === 'all') {
    return props.items
  }

  return props.items.filter(
    item => item.tipo === props.kind
  )
})
</script>

<template>
  <label class="field">
    <span class="field-label">
      {{ label }}
    </span>

    <select
      :value="modelValue"
      @change="emit('update:modelValue', $event.target.value)"
    >
      <option value="">
        {{ placeholder }}
      </option>

      <option
        v-for="item in filteredItems"
        :key="item.id_nodo"
        :value="item.id_nodo"
      >
        {{ item.nombre }} · {{ item.distrito }}
      </option>
    </select>
  </label>
</template>
