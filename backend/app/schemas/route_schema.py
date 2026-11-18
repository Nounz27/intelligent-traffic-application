from dataclasses import dataclass
from typing import Any


@dataclass
class RouteRequest:
    """Representa una solicitud de cálculo de ruta."""

    origin_id: str
    destination_id: str
    waypoint_ids: list[str]
    algorithm: str
    include_return: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RouteRequest":
        """Construye y valida una solicitud desde un diccionario."""

        if not isinstance(data, dict):
            raise ValueError("El cuerpo de la solicitud debe ser un objeto JSON.")

        origin_id = data.get("origin_id")
        destination_id = data.get("destination_id")
        waypoint_ids = data.get("waypoint_ids", [])
        algorithm = data.get("algorithm", "astar")
        include_return = data.get("include_return", False)

        if not isinstance(origin_id, str) or not origin_id.strip():
            raise ValueError("Debes seleccionar un laboratorio de origen.")

        if not isinstance(destination_id, str) or not destination_id.strip():
            raise ValueError("Debes seleccionar una farmacia de destino.")

        if not isinstance(waypoint_ids, list):
            raise ValueError("waypoint_ids debe ser una lista.")

        if not all(
            isinstance(item, str) and item.strip()
            for item in waypoint_ids
        ):
            raise ValueError("Todas las farmacias intermedias deben tener un ID válido.")

        if algorithm not in ("astar", "dijkstra"):
            raise ValueError("El algoritmo debe ser 'astar' o 'dijkstra'.")

        if not isinstance(include_return, bool):
            raise ValueError("include_return debe ser verdadero o falso.")

        return cls(
            origin_id=origin_id.strip(),
            destination_id=destination_id.strip(),
            waypoint_ids=waypoint_ids,
            algorithm=algorithm,
            include_return=include_return
        )