import networkx as nx

from app import create_app


app = create_app()

graph_data = app.extensions["graph_data"]
road_data = app.extensions["road_data"]

G = road_data["graph"]

reverse_graph = G.reverse(copy=False)

establishments = graph_data["nodes"]

mapping = road_data["establishment_road_nodes"]

candidate = None

laboratories = [
    node_id
    for node_id, node in establishments.items()
    if node["tipo"] == "laboratorio_farmaceutico"
]

pharmacies = [
    node_id
    for node_id, node in establishments.items()
    if node["tipo"] == "farmacia_botica"
]

for laboratory_id in laboratories:

    laboratory_node = mapping[laboratory_id]

    # Nodos alcanzables desde el laboratorio.
    reachable_from_lab = (
        nx.descendants(G, laboratory_node)
        | {laboratory_node}
    )

    # Nodos desde los cuales se puede regresar al laboratorio.
    can_reach_lab = (
        nx.descendants(reverse_graph, laboratory_node)
        | {laboratory_node}
    )

    for pharmacy_id in pharmacies:

        pharmacy_node = mapping[pharmacy_id]

        outbound_exists = (
            pharmacy_node in reachable_from_lab
        )

        return_exists = (
            pharmacy_node in can_reach_lab
        )

        if outbound_exists and return_exists:

            candidate = (
                laboratory_id,
                pharmacy_id
            )

            break

    if candidate:
        break


if candidate is None:

    print("No se encontró una combinación con ida y retorno.")

else:

    laboratory_id, pharmacy_id = candidate

    print("Combinación encontrada:")
    print("Laboratorio:", laboratory_id)
    print("Farmacia:", pharmacy_id)

    client = app.test_client()

    response = client.post(
        "/api/routes/compute",
        json={
            "origin_id": laboratory_id,
            "destination_id": pharmacy_id,
            "waypoint_ids": [],
            "algorithm": "astar",
            "include_return": True
        }
    )

    result = response.get_json()

    print("\nResultado de la API:")
    print("Código HTTP:", response.status_code)

    print(
        "Retorno disponible:",
        result["return_available"]
    )

    print(
        "Ruta de retorno:",
        result["return_route"]
    )