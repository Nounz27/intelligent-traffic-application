<script setup>
import { computed, onMounted, ref } from 'vue'

import {
  ArrowRight,
  RotateCcw,
  GitCompareArrows,
  Play,
  AlertCircle,
  Truck,
  SlidersHorizontal
} from 'lucide-vue-next'

import AppHeader from '../components/AppHeader.vue'
import EstablishmentSelect from '../components/EstablishmentSelect.vue'
import WaypointList from '../components/WaypointList.vue'
import RouteSummary from '../components/RouteSummary.vue'
import RouteVisualization from '../components/RouteVisualization.vue'

import { api } from '../services/api'

// DATA
const establishments = ref([])

const origin = ref('')
const destination = ref('')

const waypoints = ref([])

const algorithm = ref('astar')
const includeReturn = ref(false)

// APPLICATION STATE
const connected = ref(false)
const loading = ref(false)

const errorMessage = ref('')

const routeResult = ref(null)
const returnResult = ref(null)
const returnAvailable = ref(null)
const returnMessage = ref('')
const comparison = ref(null)

// FILTERED ESTABLISHMENTS
const laboratories = computed(() =>
  establishments.value.filter(
    item => item.tipo === 'laboratorio_farmaceutico'
  )
)

const pharmacies = computed(() =>
  establishments.value.filter(
    item => item.tipo === 'farmacia_botica'
  )
)

// LOAD DATA
onMounted(async () => {
  try {
    const [health, data] = await Promise.all([
      api.health(),
      api.getEstablishments()
    ])

    console.log('HEALTH JSON:', JSON.stringify(health))

    console.log('DATA JSON:', JSON.stringify(data))

    console.log('DATA TYPE:', typeof data)

    console.log('DATA IS ARRAY:', Array.isArray(data))

    console.log(
      'ESTABLISHMENTS:',
      data?.establishments
    )

    console.log(
      'ESTABLISHMENTS IS ARRAY:',
      Array.isArray(data?.establishments)
    )

    establishments.value =
      data.establishments || data.items || []

    console.log(
      'FINAL ESTABLISHMENTS:',
      establishments.value.length
    )

    console.log('LABORATORIES:', laboratories.value.length)

    console.log('PHARMACIES:', pharmacies.value.length)

    connected.value = Boolean(health)

  } catch (error) {
    console.error('ERROR:', error)

    connected.value = false

    errorMessage.value =
      'No se pudo conectar con Flask.'
  }
})

// WAYPOINT MANAGEMENT
function addWaypoint(id = '') {
  if (!id) return

  if (
    id === origin.value ||
    id === destination.value ||
    waypoints.value.includes(id)
  ) {
    return
  }

  waypoints.value.push(id)
}

function removeWaypoint(index) {
  waypoints.value.splice(index, 1)
}

function moveWaypoint(index, direction) {
  const target = index + direction

  if (
    target < 0 ||
    target >= waypoints.value.length
  ) {
    return
  }

  const [item] = waypoints.value.splice(index, 1)

  waypoints.value.splice(target, 0, item)
}

// VALIDATE FORM
function validateForm() {
  if (!origin.value || !destination.value) {
    return 'Selecciona un laboratorio de origen y una farmacia de destino.'
  }

  if (origin.value === destination.value) {
    return 'El origen y el destino deben ser diferentes.'
  }

  if (
    waypoints.value.includes(origin.value) ||
    waypoints.value.includes(destination.value)
  ) {
    return 'No puedes repetir el origen o destino como punto intermedio.'
  }

  return ''
}

// REQUEST DATA
function buildPayload() {
  return {
    origin_id: origin.value,
    destination_id: destination.value,

    waypoint_ids: [...waypoints.value],

    algorithm: algorithm.value,

    include_return: includeReturn.value
  }
}

// CALCULATE ROUTE
async function calculateRoute(compare = false) {
  errorMessage.value = ''

  routeResult.value = null
  returnResult.value = null
  comparison.value = null

  const validationError = validateForm()

  if (validationError) {
    errorMessage.value = validationError
    return
  }

  loading.value = true

  try {
    const payload = buildPayload()

    if (compare) {
      comparison.value = await api.compareRoutes(payload)

      const result = comparison.value.astar

      routeResult.value = result.outbound
      returnResult.value = result.return_route

      returnAvailable.value = result.return_available
      returnMessage.value = result.return_message

    } else {
      const result = await api.computeRoute(payload)

      routeResult.value = result.outbound
      returnResult.value = result.return_route

      returnAvailable.value = result.return_available
      returnMessage.value = result.return_message
    }

  } catch (error) {
    errorMessage.value =
      error.message || 'No se pudo calcular la ruta.'

  } finally {
    loading.value = false
  }

}

// RESET FORM
function resetForm() {
  origin.value = ''
  destination.value = ''

  waypoints.value = []

  algorithm.value = 'astar'
  includeReturn.value = false

  routeResult.value = null
  returnResult.value = null
  returnAvailable.value = null
  returnMessage.value = ''
  comparison.value = null

  errorMessage.value = ''
}
</script>

<template>
  <div class="app-shell">

    <AppHeader :connected="connected" />

    <main class="page-content">

      <!-- INTRODUCTION -->

      <section class="welcome">

        <div>
          <span class="eyebrow">
            PLANIFICACIÓN DE RECORRIDOS
          </span>

          <h1>
            Diseña una ruta
            <span>inteligente.</span>
          </h1>

          <p>
            Calcula el recorrido de un camión entre
            laboratorios y farmacias de Lima.
          </p>
        </div>

        <div class="welcome-icon">
          <Truck :size="29" />
        </div>

      </section>

      <!-- MAIN WORKSPACE -->

      <div class="workspace">

        <!-- CONFIGURATION -->

        <section class="config-card">

          <div class="section-heading">

            <div>
              <span class="eyebrow">
                CONFIGURACIÓN
              </span>

              <h2>Define tu recorrido</h2>
            </div>

            <SlidersHorizontal
              :size="19"
              class="muted-icon"
            />

          </div>

          <!-- ORIGIN -->

          <div class="route-step">

            <span class="step-icon origin-step">
              A
            </span>

            <EstablishmentSelect
              v-model="origin"
              label="Laboratorio de origen"
              :items="laboratories"
              kind="laboratorio_farmaceutico"
              placeholder="Seleccionar laboratorio"
            />

          </div>

          <div class="connector-line"></div>

          <!-- WAYPOINTS -->

          <WaypointList
            :items="waypoints"
            :establishments="establishments"
            @add="addWaypoint"
            @remove="removeWaypoint"
            @move="moveWaypoint"
          />

          <div class="connector-line"></div>

          <!-- DESTINATION -->

          <div class="route-step">

            <span class="step-icon destination-step">
              B
            </span>

            <EstablishmentSelect
              v-model="destination"
              label="Farmacia de destino"
              :items="pharmacies"
              kind="farmacia_botica"
              placeholder="Seleccionar farmacia o botica"
            />

          </div>

          <div class="divider"></div>

          <!-- ALGORITHM -->

          <label class="field">

            <span class="field-label">
              Algoritmo de búsqueda
            </span>

            <div class="algorithm-options">

              <button
                type="button"
                :class="{ active: algorithm === 'astar' }"
                @click="algorithm = 'astar'"
              >
                <strong>A*</strong>
                <small>Principal</small>
              </button>

              <button
                type="button"
                :class="{ active: algorithm === 'dijkstra' }"
                @click="algorithm = 'dijkstra'"
              >
                <strong>Dijkstra</strong>
                <small>Alternativo</small>
              </button>

            </div>

          </label>

          <!-- RETURN OPTION -->

          <label class="toggle-row">

            <span>
              <strong>
                Incluir retorno al laboratorio
              </strong>

              <small>
                Calcular una ruta adicional desde
                el destino hasta el origen.
              </small>
            </span>

            <input
              v-model="includeReturn"
              type="checkbox"
            />

          </label>

          <!-- ERROR MESSAGE -->

          <div
            v-if="errorMessage"
            class="error-message"
          >
            <AlertCircle :size="16" />
            {{ errorMessage }}
          </div>

          <!-- ACTION BUTTONS -->

          <div class="form-actions">

            <button
              class="primary-button"
              :disabled="loading"
              @click="calculateRoute(false)"
            >
              <Play :size="16" />

              {{ loading ? 'Calculando...' : 'Calcular ruta' }}

              <ArrowRight :size="16" />
            </button>

            <button
              class="secondary-button"
              @click="resetForm"
            >
              <RotateCcw :size="15" />
              Limpiar
            </button>

          </div>

          <button
            class="compare-button"
            :disabled="loading"
            @click="calculateRoute(true)"
          >
            <GitCompareArrows :size="16" />
            Comparar A* y Dijkstra
          </button>

        </section>

        <!-- RESULTS -->

        <div class="results-column">

          <RouteSummary
            :result="routeResult"
            :loading="loading"
          />

          <RouteVisualization
            :result="routeResult"
            :establishments="establishments"
            :selected-ids="waypoints"
          />

          <!-- RETURN ROUTE -->

          <section
            v-if="returnResult"
            class="return-card"
          >

            <span class="eyebrow">
              RECORRIDO COMPLEMENTARIO
            </span>

            <h2>Retorno al laboratorio</h2>

            <p>
              El retorno se calcula independientemente
              del recorrido de ida.
            </p>

            <div class="return-path">

              <span
                v-for="(id, index) in returnResult.path"
                :key="`${id}-${index}`"
              >
                {{ establishments.find(
                  item => item.id_nodo === id
                )?.nombre || id }}
              </span>

            </div>
          </section>

          <section
            v-if="includeReturn && returnAvailable !== null"
            class="return-card"
          >
            <span class="eyebrow">
              ESTADO DEL RETORNO
            </span>

            <h2>
            {{
              returnAvailable
              ? 'Retorno disponible'
              : 'Retorno no disponible'
            }}
            </h2>

            <p>
            {{ returnMessage }}
            </p>
          </section>
          

          <!-- COMPARISON -->

          <section
            v-if="comparison"
            class="comparison-card"
          >

            <span class="eyebrow">
              COMPARACIÓN DE ALGORITMOS
            </span>

            <h2>Resultados comparativos</h2>

            <pre>{{ JSON.stringify(comparison, null, 2) }}</pre>

          </section>

        </div>

      </div>

      <footer>
        Ruta Médica
        <span>·</span>
        Prototipo académico
      </footer>

    </main>

  </div>
</template>