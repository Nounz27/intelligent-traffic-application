from app.algorithms.astar import a_star
from app.algorithms.dijkstra import dijkstra
import osmnx as ox

def validate_establishments(
    origin_id: str,
    destination_id: str,
    waypoint_ids: list[str],
    nodes: dict
) -> None:
    """Comprueba que los establecimientos seleccionados sean válidos."""

    selected_ids = [
        origin_id,
        *waypoint_ids,
        destination_id
    ]

    if len(selected_ids) != len(set(selected_ids)):
        raise ValueError(
            "No puedes seleccionar el mismo establecimiento más de una vez."
        )

    for node_id in selected_ids:
        if node_id not in nodes:
            raise ValueError(
                f"No existe el establecimiento con ID {node_id}."
            )

    if nodes[origin_id]["tipo"] != "laboratorio_farmaceutico":
        raise ValueError("El origen debe ser un laboratorio farmacéutico.")

    pharmacy_ids = [*waypoint_ids, destination_id]

    for pharmacy_id in pharmacy_ids:
        if nodes[pharmacy_id]["tipo"] != "farmacia_botica":
            raise ValueError(
                f"El establecimiento {pharmacy_id} debe ser una farmacia."
            )

def execute_algorithm(
    algorithm: str,
    origin_id: str,
    destination_id: str,
    graph_data: dict,
    heuristic_speed_kph: float
) -> dict:
    """Ejecuta el algoritmo solicitado para un único tramo."""

    if algorithm == "astar":
        return a_star(
            origin_id,
            destination_id,
            graph_data["adjacency"],
            graph_data["coordinates"],
            heuristic_speed_kph
        )

    if algorithm == "dijkstra":
        return dijkstra(
            origin_id,
            destination_id,
            graph_data["adjacency"]
        )

    raise ValueError("Algoritmo no soportado.")

def execute_road_algorithm(
    algorithm,
    origin_node,
    destination_node,
    road_data
):

    if algorithm == "astar":
        return a_star(
            origin_node,
            destination_node,
            road_data["adjacency"],
            road_data["coordinates"],
            road_data["max_speed_kph"]
        )

    if algorithm == "dijkstra":
        return dijkstra(
            origin_node,
            destination_node,
            road_data["adjacency"]
        )

    raise ValueError("Algoritmo no soportado.")

def calculate_path_metrics(path: list[str], adjacency: dict) -> dict:
    """Acumula distancia y tiempo de las aristas de un camino."""

    total_distance = 0.0
    total_time = 0.0

    for origin_id, destination_id in zip(path, path[1:]):
        matching_edge = next(
            (
                edge
                for edge in adjacency.get(origin_id, [])
                if edge["destination"] == destination_id
            ),
            None
        )

        if matching_edge is None:
            raise ValueError(
                f"No existe la arista dirigida {origin_id} -> {destination_id}."
            )

        total_distance += matching_edge["distance"]
        total_time += matching_edge["time"]

    return {
        "distance_km": round(total_distance, 3),
        "time_min": round(total_time, 3)
    }

def build_route_geometry(road_data, path):

    if len(path) < 2:
        return []

    route_edges = ox.routing.route_to_gdf(
        road_data["graph"],
        path,
        weight="travel_time_min"
    )

    coordinates = []

    for geometry in route_edges.geometry:

        if geometry is None:
            continue

        if geometry.geom_type == "MultiLineString":
            parts = geometry.geoms
        else:
            parts = [geometry]

        for part in parts:
            for longitude, latitude in part.coords:

                point = [
                    float(latitude),
                    float(longitude)
                ]

                if not coordinates or point != coordinates[-1]:
                    coordinates.append(point)

    return coordinates

def calculate_ordered_route(
    origin_id: str,
    destination_id: str,
    waypoint_ids: list[str],
    algorithm: str,
    graph_data: dict,
    heuristic_speed_kph: float
) -> dict:
    """Calcula una ruta pasando por las farmacias en el orden indicado."""

    selected_stops = [
        origin_id,
        *waypoint_ids,
        destination_id
    ]

    complete_path = []
    total_explored_nodes = 0

    for start_id, end_id in zip(
        selected_stops,
        selected_stops[1:]
    ):
        segment = execute_algorithm(
            algorithm,
            start_id,
            end_id,
            graph_data,
            heuristic_speed_kph
        )

        segment_path = segment["path"]

        if complete_path:
            complete_path.extend(segment_path[1:])
        else:
            complete_path.extend(segment_path)

        total_explored_nodes += segment["explored_nodes"]

    metrics = calculate_path_metrics(
        complete_path,
        graph_data["adjacency"]
    )

    return {
        "algorithm": algorithm,
        "path": complete_path,
        "metrics": {
            **metrics,
            "explored_nodes": total_explored_nodes,
            "segments": len(selected_stops) - 1
        }
    }

def calculate_ordered_road_route(
    stop_ids,
    algorithm,
    establishments,
    road_data
):

    complete_path = []
    total_explored = 0

    road_adjacency = road_data["adjacency"]

    for start_id, end_id in zip(
        stop_ids,
        stop_ids[1:]
    ):

        start_node = (
            road_data["establishment_road_nodes"][start_id]
        )

        end_node = (
            road_data["establishment_road_nodes"][end_id]
        )

        segment = execute_road_algorithm(
            algorithm,
            start_node,
            end_node,
            road_data
        )

        segment_path = segment["path"]

        if complete_path:
            complete_path.extend(segment_path[1:])
        else:
            complete_path.extend(segment_path)

        total_explored += segment["explored_nodes"]

    metrics = calculate_path_metrics(
        complete_path,
        road_adjacency
    )

    # Información geográfica de los establecimientos.
    stops = []

    for index, stop_id in enumerate(stop_ids):

        establishment = establishments[stop_id]

        road_node = (
            road_data["establishment_road_nodes"][stop_id]
        )

        road_coordinate = road_data["coordinates"][road_node]

        role = (
            "origin" if index == 0
            else "destination" if index == len(stop_ids) - 1
            else "waypoint"
        )

        stops.append({
            "id": stop_id,
            "name": establishment["nombre"],
            "tipo": establishment["tipo"],
            "latitud": float(establishment["latitud"]),
            "longitud": float(establishment["longitud"]),
            "road_access": [
                road_coordinate["latitud"],
                road_coordinate["longitud"]
            ],
            "snap_distance_m": road_data["snap_distances"][stop_id],
            "role": role
        })

    return {
        "algorithm": algorithm,

        # Establecimientos seleccionados.
        "path": stop_ids,

        "stops": stops,

        # Coordenadas reales de la red vial.
        "geometry": build_route_geometry(
            road_data,
            complete_path
        ),

        "metrics": {
            **metrics,
            "explored_nodes": total_explored,
            "segments": len(stop_ids) - 1
        }
    }

def calculate_route(
    origin_id,
    destination_id,
    waypoint_ids,
    algorithm,
    include_return,
    graph_data,
    road_data
):

    validate_establishments(
        origin_id,
        destination_id,
        waypoint_ids,
        graph_data["nodes"]
    )

    outbound_stops = [
        origin_id,
        *waypoint_ids,
        destination_id
    ]

    outbound = calculate_ordered_road_route(
        outbound_stops,
        algorithm,
        graph_data["nodes"],
        road_data
    )

    return_route = None
    return_available = None
    return_message = None

    if include_return:

        try:
            return_route = calculate_ordered_road_route(
                [destination_id, origin_id],
                algorithm,
                graph_data["nodes"],
                road_data
            )

            return_available = True
            return_message = "Ruta de retorno encontrada."

        except ValueError as error:

            return_available = False
            return_message = str(error)

    return {
        "outbound": outbound,
        "return_route": return_route,
        "return_available": return_available,
        "return_message": return_message
    }
