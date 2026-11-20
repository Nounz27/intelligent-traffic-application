from flask import Flask, jsonify
from flask_cors import CORS

from app.config import Config
from app.api.establishments import establishments_bp
from app.api.routes import routes_bp
from app.services.data_service import load_graph_data
from app.services.road_network_service import (load_road_network)

def create_app(test_config=None):
    """Crea y configura la aplicación Flask."""

    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    # Permite que Vue se comunique con Flask.
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": app.config["FRONTEND_ORIGIN"]
            }
        }
    )

    # Cargar los CSV y construir el grafo al iniciar.
    graph_data = load_graph_data(
        app.config["NODES_FILE"],
        app.config["EDGES_FILE"]
    )

    road_data = load_road_network(
    app.config["ROAD_GRAPH_FILE"],
    app.config["ROAD_MAPPING_FILE"],
    graph_data["nodes"].keys()
    )

    app.extensions["road_data"] = road_data
    app.extensions["graph_data"] = graph_data

    # Registrar los endpoints.
    app.register_blueprint(establishments_bp)
    app.register_blueprint(routes_bp)

    @app.get("/api/health")
    def health_check():
        """Comprueba el estado del backend y los datos cargados."""

        return jsonify({
            "status": "ok",
            "message": "Backend funcionando correctamente.",
            "data": {
                "road_network": {
                    "nodes": road_data["node_count"],
                    "edges": road_data["edge_count"],
                    "mapped_establishments": len(
                        road_data["establishment_road_nodes"]
                    )
                }
            }
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "El recurso solicitado no existe."
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.exception("Error interno del servidor.")

        return jsonify({
            "error": "Ocurrió un error interno en el servidor."
        }), 500

    return app