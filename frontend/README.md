# Ruta Médica - Frontend

Aplicación web académica para la planificación
de rutas entre laboratorios y establecimientos
farmacéuticos de Lima Metropolitana.

## Tecnologías

- Vue 3
- JavaScript
- Vite
- Lucide Vue Next
- CSS

## Requisitos

- Node.js
- npm

## Instalación

npm install

## Ejecución

npm run dev

## Compilación

npm run build

## Backend

La aplicación está preparada para comunicarse
con un backend desarrollado en Python y Flask.

Dirección predeterminada:

http://127.0.0.1:5000/api

## Funcionalidades

- Selección de laboratorio de origen.
- Selección de farmacia de destino.
- Selección de farmacias intermedias.
- Reordenamiento de puntos intermedios.
- Selección de algoritmo A* o Dijkstra.
- Retorno opcional al laboratorio.
- Visualización de resultados.
- Comparación de algoritmos.

## Alcance

El frontend no implementa los algoritmos de
búsqueda ni genera rutas ficticias.

Los cálculos serán realizados exclusivamente
por el backend.