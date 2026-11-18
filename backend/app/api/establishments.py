from flask import Blueprint, current_app, jsonify, request

establishments_bp = Blueprint(
    "establishments",
    __name__,
    url_prefix="/api/establishments"
)

@establishments_bp.get("")
def get_establishments():
    """Devuelve los establecimientos disponibles."""

    graph_data = current_app.extensions["graph_data"]
    establishments = list(graph_data["nodes"].values())

    establishment_type = request.args.get("type")
    search = request.args.get("q", "").strip().lower()

    if establishment_type:
        establishments = [
            item for item in establishments
            if item["tipo"] == establishment_type
        ]

    if search:
        establishments = [
            item for item in establishments
            if search in item["id_nodo"].lower()
            or search in item["nombre"].lower()
            or search in item["distrito"].lower()
        ]

    return jsonify({
        "establishments": establishments,
        "total": len(establishments)
    })