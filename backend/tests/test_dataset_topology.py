from app.config import Config

from app.services.data_service import (
    load_graph_data
)


def test_abstract_graph_has_no_incoming_edges_to_labs():

    graph_data = load_graph_data(
        Config.NODES_FILE,
        Config.EDGES_FILE
    )

    lab_ids = {
        node_id
        for node_id, node in graph_data["nodes"].items()
        if node["tipo"] == "laboratorio_farmaceutico"
    }

    incoming_edges = [
        edge
        for edges in graph_data["adjacency"].values()
        for edge in edges
        if edge["destination"] in lab_ids
    ]

    assert incoming_edges == []