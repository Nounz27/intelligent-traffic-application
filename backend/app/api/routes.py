from flask import Blueprint, current_app, jsonify, request

from app.schemas.route_schema import RouteRequest
from app.services.route_service import calculate_route

routes_bp = Blueprint(
    "routes",
    __name__,
    url_prefix="/api/routes"
)

def get_route_request():
    """Obtiene y valida los datos JSON de una solicitud."""

    data = request.get_json(silent=True)

    if data is None:
        raise ValueError("Debes enviar un cuerpo JSON válido.")

    return RouteRequest.from_dict(data)

def calculate_for_algorithm(route_request, algorithm: str):
    """Ejecuta el cálculo con un algoritmo específico."""

    graph_data = current_app.extensions["graph_data"]

    return calculate_route(
        origin_id=route_request.origin_id,
        destination_id=route_request.destination_id,
        waypoint_ids=route_request.waypoint_ids,
        algorithm=algorithm,
        include_return=route_request.include_return,
        graph_data=graph_data,
        heuristic_speed_kph=current_app.config[
            "HEURISTIC_SPEED_KPH"
        ]
    )

@routes_bp.post("/compute")
def compute_route():
    """Calcula una ruta con el algoritmo seleccionado."""

    try:
        route_request = get_route_request()

        result = calculate_for_algorithm(
            route_request,
            route_request.algorithm
        )

        return jsonify(result), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

@routes_bp.post("/compare")
def compare_routes():
    """Compara A* y Dijkstra para la misma solicitud."""

    try:
        route_request = get_route_request()

        astar_result = calculate_for_algorithm(
            route_request,
            "astar"
        )

        dijkstra_result = calculate_for_algorithm(
            route_request,
            "dijkstra"
        )

        return jsonify({
            "astar": astar_result,
            "dijkstra": dijkstra_result
        }), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400