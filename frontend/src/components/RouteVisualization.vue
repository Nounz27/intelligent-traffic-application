<script setup>
import { computed } from 'vue'

import {
  Map as MapIcon,
  Info
} from 'lucide-vue-next'

const props = defineProps({
  result: {
    type: Object,
    default: null
  },

  establishments: {
    type: Array,
    default: () => []
  },

  selectedIds: {
    type: Array,
    default: () => []
  }
})

const path = computed(() =>
  props.result?.path ??
  props.result?.ruta ??
  []
)

function nameFor(id) {
  const establishment = props.establishments.find(
    item => item.id_nodo === id
  )

  return establishment?.nombre || id
}
</script>

<template>
  <section class="visual-card">

    <div class="section-heading">
      <div>
        <span class="eyebrow">VISUALIZACIÓN</span>
        <h2>Recorrido calculado</h2>
      </div>

      <span class="graph-label">
        <MapIcon :size="14" />
        Grafo esquemático
      </span>
    </div>

    <div
      v-if="path.length"
      class="route-path"
    >

      <div
        v-for="(id, index) in path"
        :key="`${id}-${index}`"
        class="path-item"
      >

        <span
          class="path-marker"
          :class="{
            origin: index === 0,
            destination: index === path.length - 1
          }"
        >
          {{ index + 1 }}
        </span>

        <div>
          <strong>{{ nameFor(id) }}</strong>

          <small>
            {{ id }} ·

            {{
              index === 0
                ? 'Origen'
                : index === path.length - 1
                  ? 'Destino'
                  : selectedIds.includes(id)
                    ? 'Punto intermedio'
                    : 'Tránsito'
            }}
          </small>
        </div>

      </div>

    </div>

    <div
      v-else
      class="canvas-placeholder"
    >
      <div class="placeholder-network">
        <span class="node n1"></span>
        <span class="node n2"></span>
        <span class="node n3"></span>
        <span class="node n4"></span>

        <span class="edge e1"></span>
        <span class="edge e2"></span>
        <span class="edge e3"></span>
      </div>

      <strong>
        Tu recorrido aparecerá aquí
      </strong>

      <p>
        Calcula una ruta para visualizar su secuencia.
      </p>
    </div>

    <div class="legend">
      <span>
        <i class="legend-dot origin"></i>
        Origen
      </span>

      <span>
        <i class="legend-dot middle"></i>
        Intermedio
      </span>

      <span>
        <i class="legend-dot destination"></i>
        Destino
      </span>

      <span>
        <i class="legend-dot transit"></i>
        Tránsito
      </span>
    </div>

    <div class="info-note">
      <Info :size="15" />

      Esta vista representa conexiones del grafo
      abstracto, no calles ni trayectorias geográficas.
    </div>

  </section>
</template>
