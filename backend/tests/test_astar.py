from app.algorithms.astar import a_star

def test_astar_finds_shortest_path():
    adjacency = {
        "A": [
            {"destination": "B", "time": 5, "distance": 2},
            {"destination": "C", "time": 2, "distance": 1}
        ],
        "B": [
            {"destination": "D", "time": 2, "distance": 1}
        ],
        "C": [
            {"destination": "B", "time": 1, "distance": 1},
            {"destination": "D", "time": 8, "distance": 3}
        ],
        "D": []
    }

    coordinates = {
        "A": {"latitud": 0.0, "longitud": 0.0},
        "B": {"latitud": 0.0, "longitud": 0.0},
        "C": {"latitud": 0.0, "longitud": 0.0},
        "D": {"latitud": 0.0, "longitud": 0.0}
    }

    result = a_star(
        "A",
        "D",
        adjacency,
        coordinates
    )

    assert result["path"] == ["A", "C", "B", "D"]
    assert result["cost"] == 5