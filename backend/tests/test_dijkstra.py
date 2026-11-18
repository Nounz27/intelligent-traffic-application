from app.algorithms.dijkstra import dijkstra

def test_dijkstra_finds_shortest_path():
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

    result = dijkstra("A", "D", adjacency)

    assert result["path"] == ["A", "C", "B", "D"]
    assert result["cost"] == 5