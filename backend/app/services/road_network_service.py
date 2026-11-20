import math
from collections import defaultdict
from pathlib import Path

import osmnx as ox
import pandas as pd

def load_road_network(
    graphml_file: Path,
    mapping_file: Path,
    establishment_ids
) -> dict:

    if not graphml_file.exists():
        raise FileNotFoundError(
            f"No se encontró la red vial: {graphml_file}"
        )

    if not mapping_file.exists():
        raise FileNotFoundError(
            f"No se encontró el mapeo vial: {mapping_file}"
        )

    # Cargar la red dirigida.
    graph = ox.io.load_graphml(
        filepath=graphml_file
    )

    if not graph.is_directed():
        raise ValueError(
            "La red vial debe ser dirigida."
        )

    # Coordenadas de los nodos viales.
    coordinates = {
        node_id: {
            "latitud": float(data["y"]),
            "longitud": float(data["x"])
        }
        for node_id, data in graph.nodes(data=True)
    }

    # Seleccionar la arista de menor tiempo
    # cuando existen varias conexiones entre u y v.
    best_edges = {}

    for u, v, key, data in graph.edges(
        keys=True,
        data=True
    ):
        time_min = float(data["travel_time_min"])

        if not math.isfinite(time_min) or time_min <= 0:
            continue

        edge = {
            "time": time_min,
            "distance": float(data["length"]) / 1000
        }

        current = best_edges.get((u, v))

        if current is None or time_min < current["time"]:
            best_edges[(u, v)] = edge

    # Construir la adyacencia dirigida.
    adjacency = defaultdict(list)

    for (u, v), edge in best_edges.items():
        adjacency[u].append({
            "destination": v,
            "time": edge["time"],
            "distance": edge["distance"]
        })

    # Cargar asociación establecimiento -> nodo vial.
    mapping_df = pd.read_csv(mapping_file)

    required = {
        "id_nodo",
        "nodo_vial_cercano",
        "distancia_establecimiento_a_nodo_vial_m"
    }

    missing_columns = required - set(mapping_df.columns)

    if missing_columns:
        raise ValueError(
            f"Faltan columnas en el mapeo vial: {missing_columns}"
        )

    establishment_road_nodes = {}
    snap_distances = {}

    for row in mapping_df.to_dict(orient="records"):

        establishment_id = str(row["id_nodo"])
        road_node = int(row["nodo_vial_cercano"])

        if road_node not in coordinates:
            raise ValueError(
                f"El nodo vial {road_node} no existe."
            )

        establishment_road_nodes[establishment_id] = road_node

        snap_distances[establishment_id] = float(
            row["distancia_establecimiento_a_nodo_vial_m"]
        )

    missing_establishments = (
        set(establishment_ids)
        - set(establishment_road_nodes)
    )

    if missing_establishments:
        raise ValueError(
            "Hay establecimientos sin asociación vial."
        )

    # Velocidad máxima para una heurística admisible de A*.
    max_speed = max(
        float(data["speed_kph"])
        for _, _, _, data in graph.edges(
            keys=True,
            data=True
        )
    )

    return {
        "graph": graph,
        "adjacency": dict(adjacency),
        "coordinates": coordinates,
        "establishment_road_nodes": establishment_road_nodes,
        "snap_distances": snap_distances,
        "max_speed_kph": max_speed,
        "node_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges()
    }
