<script setup>
import {
  Route,
  Clock3,
  Activity,
  Navigation
} from 'lucide-vue-next'

const props = defineProps({
  result: {
    type: Object,
    default: null
  },

  loading: {
    type: Boolean,
    default: false
  }
})

function format(value, suffix) {
  const number = Number(value)

  return Number.isFinite(number)
    ? `${number.toFixed(2)} ${suffix}`
    : '—'
}

function metric(primary, secondary) {
  return props.result?.metrics?.[primary]
    ?? props.result?.[primary]
    ?? props.result?.metrics?.[secondary]
    ?? props.result?.[secondary]
}
</script>

<template>
  <section class="summary-card">

    <div class="section-heading">
      <div>
        <span class="eyebrow">RESULTADO</span>
        <h2>Resumen de ruta</h2>
      </div>

      <span
        v-if="result"
        class="success-tag"
      >
        Calculada
      </span>
    </div>

    <div
      v-if="loading"
      class="loading-state"
    >
      Calculando recorrido...
    </div>

    <div
      v-else-if="result"
      class="metric-grid"
    >

      <div class="metric">
        <span class="metric-icon blue">
          <Route :size="17" />
        </span>

        <span class="metric-label">
          Distancia
        </span>

        <strong>
          {{ format(
            metric('distance_km', 'distancia_km'),
            'km'
          ) }}
        </strong>
      </div>

      <div class="metric">
        <span class="metric-icon green">
          <Clock3 :size="17" />
        </span>

        <span class="metric-label">
          Tiempo estimado
        </span>

        <strong>
          {{ format(
            metric('time_min', 'tiempo_min'),
            'min'
          ) }}
        </strong>
      </div>

      <div class="metric">
        <span class="metric-icon red">
          <Activity :size="17" />
        </span>

        <span class="metric-label">
          Nodos explorados
        </span>

        <strong>
          {{ metric(
            'explored_nodes',
            'nodos_explorados'
          ) ?? '—' }}
        </strong>
      </div>

      <div class="metric">
        <span class="metric-icon violet">
          <Navigation :size="17" />
        </span>

        <span class="metric-label">
          Tramos
        </span>

        <strong>
          {{ metric('segments', 'tramos') ?? '—' }}
        </strong>
      </div>

    </div>

    <div
      v-else
      class="empty-result"
    >
      <div class="empty-icon">
        <Route :size="22" />
      </div>

      <strong>Aún no hay una ruta</strong>

      <p>
        Configura el origen y destino para visualizar
        el resultado aquí.
      </p>
    </div>

    <p class="disclaimer">
      Los tiempos y distancias son estimaciones del
      grafo abstracto. No representan tráfico en
      tiempo real ni navegación por calles.
    </p>

  </section>
</template>
