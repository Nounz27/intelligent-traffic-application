import heapq
import math

def dijkstra(
    origin_id: str,
    destination_id: str,
    adjacency: dict
) -> dict:
    """
    Encuentra la ruta de menor tiempo estimado mediante Dijkstra.

    Retorna:
        path: secuencia de IDs.
        cost: tiempo total estimado en minutos.
        explored_nodes: cantidad de nodos explorados.
    """

    if origin_id == destination_id:
        return {
            "path": [origin_id],
            "cost": 0.0,
            "explored_nodes": 0
        }

    frontier = [(0.0, origin_id)]

    costs = {origin_id: 0.0}
    previous = {}

    explored = set()

    while frontier:
        current_cost, current_id = heapq.heappop(frontier)

        if current_cost > costs.get(current_id, math.inf):
            continue

        if current_id in explored:
            continue

        explored.add(current_id)

        if current_id == destination_id:
            path = []
            node_id = destination_id

            while node_id != origin_id:
                path.append(node_id)
                node_id = previous[node_id]

            path.append(origin_id)
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

                heapq.heappush(
                    frontier,
                    (new_cost, neighbor_id)
                )

    raise ValueError(
        f"No se encontró una ruta entre {origin_id} y {destination_id}."
    )