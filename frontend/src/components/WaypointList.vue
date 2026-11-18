<script setup>
import { computed } from 'vue'

import {
  X,
  ChevronUp,
  ChevronDown,
  MapPin
} from 'lucide-vue-next'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },

  establishments: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits([
  'add',
  'remove',
  'move'
])

const pharmacies = computed(() =>
  props.establishments.filter(
    item => item.tipo === 'farmacia_botica'
  )
)

function nameFor(id) {
  const establishment = props.establishments.find(
    item => item.id_nodo === id
  )

  return establishment?.nombre || id
}
</script>

<template>
  <div class="waypoints">

    <div class="waypoint-heading">
      <div>
        <span class="field-label">
          Farmacias intermedias
        </span>

        <p>
          El camión pasará por ellas en el orden indicado.
        </p>
      </div>
    </div>

    <div
      v-if="items.length"
      class="waypoint-items"
    >
      <div
        v-for="(id, index) in items"
        :key="id"
        class="waypoint-row"
      >
        <span class="waypoint-number">
          {{ index + 1 }}
        </span>

        <span class="waypoint-name">
          <MapPin :size="14" />
          {{ nameFor(id) }}
        </span>

        <div class="waypoint-actions">

          <button
            class="tiny-button"
            :disabled="index === 0"
            @click="emit('move', index, -1)"
          >
            <ChevronUp :size="15" />
          </button>

          <button
            class="tiny-button"
            :disabled="index === items.length - 1"
            @click="emit('move', index, 1)"
          >
            <ChevronDown :size="15" />
          </button>

          <button
            class="tiny-button remove"
            @click="emit('remove', index)"
          >
            <X :size="15" />
          </button>

        </div>
      </div>
    </div>

    <div
      v-else
      class="empty-waypoints"
    >
      No has añadido farmacias intermedias.
    </div>

    <select
      class="add-select"
      @change="
        event => {
          if (event.target.value) {
            emit('add', event.target.value)
          }

          event.target.value = ''
        }
      "
    >
      <option value="">
        Añadir una farmacia...
      </option>

      <option
        v-for="item in pharmacies"
        :key="item.id_nodo"
        :value="item.id_nodo"
      >
        {{ item.nombre }} · {{ item.distrito }}
      </option>
    </select>

  </div>
</template>
