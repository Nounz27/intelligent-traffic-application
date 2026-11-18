import heapq
import math

from app.utils.geo import haversine_km


def a_star(
    origin_id: str,
    destination_id: str,
    adjacency: dict,
    coordinates: dict,
    heuristic_speed_kph: float = 60.0
) -> dict:
    """
    Encuentra la ruta de menor tiempo estimado mediante A*.

    Retorna:
        path: secuencia de IDs.
        cost: tiempo total estimado en minutos.
        explored_nodes: cantidad de nodos explorados.
    """

    if origin_id not in coordinates:
        raise ValueError(f"No existe el nodo de origen: {origin_id}")

    if destination_id not in coordinates:
        raise ValueError(f"No existe el nodo de destino: {destination_id}")

    if origin_id == destination_id:
        return {
            "path": [origin_id],
            "cost": 0.0,
            "explored_nodes": 0
        }

    def heuristic(current_id: str) -> float:
        current = coordinates[current_id]
        destination = coordinates[destination_id]

        distance = haversine_km(
            current["latitud"],
            current["longitud"],
            destination["latitud"],
            destination["longitud"]
        )

        return distance / heuristic_speed_kph * 60

    frontier = [
        (heuristic(origin_id), 0.0, origin_id)
    ]

    costs = {origin_id: 0.0}
    previous = {origin_id: None}

    explored = set()

    while frontier:
        _, current_cost, current_id = heapq.heappop(frontier)

        if current_cost > costs.get(current_id, math.inf):
            continue

        if current_id in explored:
            continue

        explored.add(current_id)

        if current_id == destination_id:
            path = []
            node_id = destination_id

            while node_id is not None:
                path.append(node_id)
                node_id = previous[node_id]

            path.reverse()

            return {
                "path": path,
                "cost": current_cost,
                "explored_nodes": len(explored)
            }

        for edge in adjacency.get(current_id, []):
            neighbor_id = edge["destination"]
            edge_cost = edge["time"]

            new_cost = current_cost + edge_cost

            if new_cost < costs.get(neighbor_id, math.inf):
                costs[neighbor_id] = new_cost
                previous[neighbor_id] = current_id

                priority = new_cost + heuristic(neighbor_id)

                heapq.heappush(
                    frontier,
                    (priority, new_cost, neighbor_id)
                )

    raise ValueError(
        f"No se encontró una ruta entre {origin_id} y {destination_id}."
    )