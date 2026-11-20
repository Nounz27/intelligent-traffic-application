from app.algorithms.dijkstra import dijkstra


def test_dijkstra_finds_directed_return_path():

    adjacency = {

        "L": [
            {
                "destination": "F1",
                "distance": 1,
                "time": 2
            }
        ],

        "F1": [
            {
                "destination": "F2",
                "distance": 1,
                "time": 2
            },
            {
                "destination": "L",
                "distance": 1,
                "time": 3
            }
        ],

        "F2": [
            {
                "destination": "F1",
                "distance": 1,
                "time": 2
            }
        ]
    }

    result = dijkstra(
        "F2",
        "L",
        adjacency
    )

    assert result["path"] == [
        "F2",
        "F1",
        "L"
    ]

    assert result["cost"] == 5