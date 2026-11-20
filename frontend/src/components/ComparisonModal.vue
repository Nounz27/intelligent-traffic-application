<script setup>
import { computed } from 'vue'
import { X, GitCompareArrows } from 'lucide-vue-next'

import RouteSummary from './RouteSummary.vue'
import RouteVisualization from './RouteVisualization.vue'

const props = defineProps({
  astar: {
    type: Object,
    required: true
  },
  dijkstra: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close'])

function getMetric(result, primary, secondary) {
  return Number(
    result?.metrics?.[primary] ??
    result?.[primary] ??
    result?.metrics?.[secondary] ??
    result?.[secondary] ??
    0
  )
}

const differences = computed(() => {
  const a = props.astar
  const d = props.dijkstra

  const timeA = getMetric(a, 'time_min', 'tiempo_min')
  const timeD = getMetric(d, 'time_min', 'tiempo_min')

  const distanceA = getMetric(a, 'distance_km', 'distancia_km')
  const distanceD = getMetric(d, 'distance_km', 'distancia_km')

  const exploredA = getMetric(a, 'explored_nodes', 'nodos_explorados')
  const exploredD = getMetric(d, 'explored_nodes', 'nodos_explorados')

  const formatDifference = (value, suffix) =>
    `${Math.abs(value).toFixed(2)} ${suffix}`

  const faster =
    timeA < timeD ? 'A*' :
    timeD < timeA ? 'Dijkstra' : 'Ambos algoritmos'

  const fewerNodes =
    exploredA < exploredD ? 'A*' :
    exploredD < exploredA ? 'Dijkstra' : 'Ambos algoritmos'

  return {
    faster,
    fewerNodes,
    timeDifference: formatDifference(
      timeA - timeD,
      'min'
    ),
    distanceDifference: formatDifference(
      distanceA - distanceD,
      'km'
    )
  }
})
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">

    <section
      class="comparison-modal"
      role="dialog"
      aria-modal="true"
      aria-labelledby="comparison-title"
    >

      <header class="modal-header">

        <div>
          <span class="eyebrow">
            ANÁLISIS DE RENDIMIENTO
          </span>

          <h2 id="comparison-title">
            Comparación de algoritmos
          </h2>

          <p>
            Resultados de A* y Dijkstra para el mismo recorrido.
          </p>
        </div>

        <button
          class="close-button"
          type="button"
          aria-label="Cerrar comparación"
          @click="emit('close')"
        >
          <X :size="21" />
        </button>

      </header>

      <div class="modal-content">

        <!-- ROUTE SUMMARIES -->

        <section class="comparison-summaries">

          <div class="algorithm-result">
            <div class="algorithm-heading">
              <GitCompareArrows :size="18" />
              <h3>A*</h3>
            </div>

            <RouteSummary
              :result="astar"
              title="Resumen A*"
            />
          </div>

          <div class="algorithm-result">
            <div class="algorithm-heading">
              <GitCompareArrows :size="18" />
              <h3>Dijkstra</h3>
            </div>

            <RouteSummary
              :result="dijkstra"
              title="Resumen Dijkstra"
            />
          </div>

        </section>

        <!-- MAP -->

        <section class="comparison-map-section">

          <div class="section-heading">
            <div>
              <span class="eyebrow">
                VISUALIZACIÓN GEOGRÁFICA
              </span>

              <h3>Comparación de recorridos</h3>
            </div>
          </div>

          <!-- Este componente debe aceptar ambos resultados
               y dibujar sus geometrías en el mismo mapa. -->

          <RouteVisualization
            :result="astar"
            :comparison-result="dijkstra"
            comparison-mode
          />

          <div class="map-legend">
            <span>
              <i class="legend-line astar-line"></i>
              A*
            </span>

            <span>
              <i class="legend-line dijkstra-line"></i>
              Dijkstra
            </span>
          </div>

        </section>

        <!-- DIFFERENCES -->

        <section class="difference-section">

          <span class="eyebrow">
            ANÁLISIS DE DIFERENCIAS
          </span>

          <p>
            <strong>Tiempo:</strong>
            {{ differences.faster }} presentó el menor tiempo.
          </p>

          <p>
            <strong>Exploración:</strong>
            {{ differences.fewerNodes }} exploró menos nodos.
          </p>

          <p>
            <strong>Diferencia de distancia:</strong>
            {{ differences.distanceDifference }}.
          </p>

          <p>
            <strong>Diferencia de tiempo:</strong>
            {{ differences.timeDifference }}.
          </p>

        </section>

      </div>

      <footer class="modal-footer">

        <button
          type="button"
          class="primary-button"
          @click="emit('close')"
        >
          Cerrar comparación
        </button>

      </footer>

    </section>

  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;

  display: flex;
  justify-content: center;
  align-items: center;

  padding: 24px;

  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(4px);
}

.comparison-modal {
  width: 100%;
  max-width: 1050px;
  max-height: 92vh;

  display: flex;
  flex-direction: column;

  background: white;
  border-radius: 20px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;

  padding: 24px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h2 {
  margin: 7px 0;
  font-size: 23px;
}

.modal-header p {
  color: #64748b;
  font-size: 13px;
}

.close-button {
  border: none;
  background: #f1f5f9;
  border-radius: 9px;
  padding: 9px;
  cursor: pointer;
}

.modal-content {
  overflow-y: auto;
  padding: 24px;
}

.comparison-summaries {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.algorithm-result {
  min-width: 0;
}

.algorithm-heading {
  display: flex;
  align-items: center;
  gap: 9px;
  margin-bottom: 12px;
}

.algorithm-heading h3 {
  margin: 0;
  font-size: 17px;
}

.comparison-map-section {
  margin-top: 28px;
}

.comparison-map-section h3 {
  margin-top: 6px;
}

.map-legend {
  display: flex;
  gap: 22px;
  margin-top: 12px;
  font-size: 12px;
  color: #64748b;
}

.map-legend span {
  display: flex;
  align-items: center;
  gap: 7px;
}

.legend-line {
  width: 23px;
  height: 4px;
  border-radius: 4px;
}

.astar-line {
  background: #f59e0b;
}

.dijkstra-line {
  background: #2563eb;
}

.difference-section {
  margin-top: 25px;
  padding: 18px;

  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
}

.difference-section p {
  font-size: 13px;
  color: #475569;
  margin: 10px 0 0;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;

  padding: 18px 24px;
  border-top: 1px solid #e2e8f0;
}

@media (max-width: 700px) {
  .modal-overlay {
    padding: 10px;
  }

  .comparison-modal {
    max-height: 96vh;
  }

  .comparison-summaries {
    grid-template-columns: 1fr;
  }

  .modal-header,
  .modal-content {
    padding: 16px;
  }
}
</style>