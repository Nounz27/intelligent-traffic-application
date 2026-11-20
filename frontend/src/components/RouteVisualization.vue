<script setup>
import {
  onMounted,
  onBeforeUnmount,
  ref,
  watch
} from 'vue'

import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  result: {
    type: Object,
    default: null
  },

  returnResult: {
    type: Object,
    default: null
  },

  comparisonResult: {
    type: Object,
    default: null
  },

  comparisonMode: {
    type: Boolean,
    default: false
  }
})

const mapElement = ref(null)

let map = null
let routeLayer = null

const LIMA_CENTER = [-12.0464, -77.0428]

// Dibujar una ruta sobre el mapa.
function addRoute(result, color, dashArray, bounds) {

  const geometry = result?.geometry ?? []

  if (geometry.length < 2) {
    return
  }

  L.polyline(geometry, {
    color,
    weight: 5,
    opacity: 0.9,
    dashArray
  }).addTo(routeLayer)

  bounds.push(...geometry)

  if (props.comparisonMode && props.comparisonResult) {

  const dijkstraGeometry =
    props.comparisonResult.geometry ?? []

  if (dijkstraGeometry.length >= 2) {

    L.polyline(dijkstraGeometry, {
      color: '#2563EB',
      weight: 5,
      opacity: 0.9,
      dashArray: '8 7'
    }).addTo(routeLayer)

    bounds.push(...dijkstraGeometry)
  }
}
}

// Crear un marcador de establecimiento.
function addStop(stop, bounds) {

  const point = [
    stop.latitud,
    stop.longitud
  ]

  const colors = {
    origin: '#DC2626',
    waypoint: '#2563EB',
    destination: '#16A34A'
  }

  const color = colors[stop.role] || '#64748B'

  // Mostrar el conector entre el establecimiento
  // y su nodo vial asociado.
  if (stop.road_access) {

    L.polyline(
      [point, stop.road_access],
      {
        color: '#64748B',
        weight: 2,
        opacity: 0.8,
        dashArray: '4 6'
      }
    ).addTo(routeLayer)

    bounds.push(stop.road_access)
  }

  const marker = L.circleMarker(point, {
    radius: 8,
    color: '#FFFFFF',
    weight: 2,
    fillColor: color,
    fillOpacity: 1
  }).addTo(routeLayer)

  // Crear el popup sin insertar HTML externo directamente.
  const popup = document.createElement('div')

  const title = document.createElement('strong')
  title.textContent = stop.name

  const details = document.createElement('div')
  details.textContent = `${stop.id} · ${stop.tipo}`

  popup.append(title, details)

  marker.bindPopup(popup)

  bounds.push(point)
}

// Actualizar las capas del mapa.
function renderRoutes() {

  if (!map || !routeLayer) {
    return
  }

  routeLayer.clearLayers()

  const bounds = []

  // Recorrido de ida.
  addRoute(
    props.result,
    '#F59E0B',
    null,
    bounds
  )

  // Recorrido de retorno.
  addRoute(
    props.returnResult,
    '#2563EB',
    '8 7',
    bounds
  )

  // Marcadores de los establecimientos de ida.
  for (const stop of props.result?.stops ?? []) {
    addStop(stop, bounds)
  }

  // Ajustar el mapa a la ruta calculada.
  if (bounds.length > 0) {

    map.fitBounds(
      L.latLngBounds(bounds),
      {
        padding: [30, 30],
        maxZoom: 15
      }
    )
  }
}

// Inicializar el mapa cuando Vue haya creado el elemento DOM.
onMounted(() => {

  map = L.map(mapElement.value).setView(
    LIMA_CENTER,
    11
  )

  L.tileLayer(
    import.meta.env.VITE_MAP_TILE_URL ||
      'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
      maxZoom: 19,

      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">' +
        'OpenStreetMap</a> contributors'
    }
  ).addTo(map)

  routeLayer = L.layerGroup().addTo(map)

  renderRoutes()
})

// Actualizar las rutas cuando cambien las propiedades.
watch(
  () => [props.result, props.returnResult],
  renderRoutes,
  { deep: true }
)

// Liberar los recursos del mapa.
onBeforeUnmount(() => {

  if (map) {
    map.remove()
    map = null
    routeLayer = null
  }

})
</script>

<template>
  <section class="visual-card">

    <div class="section-heading">

      <div>
        <span class="eyebrow">
          VISUALIZACIÓN GEOGRÁFICA
        </span>

        <h2>Mapa de recorridos</h2>
      </div>

      <span class="graph-label">
        Red vial de Lima
      </span>

    </div>

    <div
      ref="mapElement"
      class="route-map"
      role="region"
      aria-label="Mapa de recorridos de distribución"
    ></div>

    <div class="map-legend">

      <span>
        <i class="legend-line outbound"></i>
        Ida
      </span>

      <span>
        <i class="legend-line returning"></i>
        Retorno
      </span>

      <span>
        <i class="legend-dot origin"></i>
        Laboratorio
      </span>

      <span>
        <i class="legend-dot destination"></i>
        Farmacia
      </span>

      <span>
        <i class="legend-line access"></i>
        Acceso al establecimiento
      </span>

    </div>

  </section>
</template>

<style scoped>
.route-map {
  width: 100%;
  height: 480px;
  border-radius: 14px;
  z-index: 0;
}

.map-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 18px;
  font-size: 12px;
  color: #64748b;
}

.map-legend span {
  display: flex;
  align-items: center;
  gap: 7px;
}

.legend-line {
  width: 22px;
  height: 4px;
  border-radius: 4px;
}

.outbound {
  background: #F59E0B;
}

.returning {
  background: #2563EB;
}

.access {
  height: 0;
  border-top: 2px dashed #64748b;
}

.legend-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
}

.origin {
  background: #DC2626;
}

.destination {
  background: #16A34A;
}

@media (max-width: 768px) {
  .route-map {
    height: 360px;
  }
}
</style>
