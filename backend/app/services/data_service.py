import pandas as pd

from collections import defaultdict
from pathlib import Path

NODE_COLUMNS = [
    "id_nodo",
    "tipo",
    "nombre",
    "latitud",
    "longitud",
    "distrito",
    "direccion"
]

EDGE_COLUMNS = [
    "origen",
    "destino",
    "distancia_ruta_estimada_km",
    "tiempo_estimado_min"
]

def load_graph_data(
    nodes_file: Path,
    edges_file: Path
) -> dict:
    """
    Carga los establecimientos y las aristas desde los CSV.

    Construye:
        nodes: información de establecimientos por ID.
        adjacency: lista de adyacencia dirigida.
        coordinates: coordenadas por ID.
    """

    if not nodes_file.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de nodos: {nodes_file}"
        )

    if not edges_file.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de aristas: {edges_file}"
        )

    nodes_df = pd.read_csv(nodes_file)
    edges_df = pd.read_csv(edges_file)

    missing_node_columns = set(NODE_COLUMNS) - set(nodes_df.columns)
    missing_edge_columns = set(EDGE_COLUMNS) - set(edges_df.columns)

    if missing_node_columns:
        raise ValueError(
            f"Faltan columnas en el CSV de nodos: {missing_node_columns}"
        )

    if missing_edge_columns:
        raise ValueError(
            f"Faltan columnas en el CSV de aristas: {missing_edge_columns}"
        )

    nodes_df = nodes_df[NODE_COLUMNS].copy()
    edges_df = edges_df[EDGE_COLUMNS].copy()

    nodes_df["id_nodo"] = nodes_df["id_nodo"].astype(str)
    edges_df["origen"] = edges_df["origen"].astype(str)
    edges_df["destino"] = edges_df["destino"].astype(str)

    numeric_node_columns = ["latitud", "longitud"]

    for column in numeric_node_columns:
        nodes_df[column] = pd.to_numeric(
            nodes_df[column],
            errors="coerce"
        )

    numeric_edge_columns = [
        "distancia_ruta_estimada_km",
        "tiempo_estimado_min"
    ]

    for column in numeric_edge_columns:
        edges_df[column] = pd.to_numeric(
            edges_df[column],
            errors="coerce"
        )

    if nodes_df["id_nodo"].duplicated().any():
        raise ValueError("El CSV de nodos contiene IDs duplicados.")

    if nodes_df[["latitud", "longitud"]].isna().any().any():
        raise ValueError("Existen coordenadas vacías o no numéricas.")

    if edges_df[numeric_edge_columns].isna().any().any():
        raise ValueError("Existen pesos de aristas vacíos o no numéricos.")

    if (edges_df[numeric_edge_columns] < 0).any().any():
        raise ValueError("Los pesos de las aristas no pueden ser negativos.")

    # Reemplazar valores vacíos de los campos de texto.
    text_node_columns = [
    "tipo",
    "nombre",
    "distrito",
    "direccion"
    ]

    for column in text_node_columns:
        nodes_df[column] = nodes_df[column].fillna("")

    node_ids = set(nodes_df["id_nodo"])

    unknown_origins = set(edges_df["origen"]) - node_ids
    unknown_destinations = set(edges_df["destino"]) - node_ids

    if unknown_origins or unknown_destinations:
        raise ValueError("Hay aristas que apuntan a nodos inexistentes.")

    nodes = {
        row["id_nodo"]: row
        for row in nodes_df.to_dict(orient="records")
    }

    coordinates = {
        node_id: {
            "latitud": float(node["latitud"]),
            "longitud": float(node["longitud"])
        }
        for node_id, node in nodes.items()
    }

    adjacency = defaultdict(list)

    for edge in edges_df.to_dict(orient="records"):
        adjacency[edge["origen"]].append({
            "destination": edge["destino"],
            "distance": float(edge["distancia_ruta_estimada_km"]),
            "time": float(edge["tiempo_estimado_min"])
        })

    return {
        "nodes": nodes,
        "adjacency": dict(adjacency),
        "coordinates": coordinates,
        "node_count": len(nodes),
        "edge_count": len(edges_df)
    }