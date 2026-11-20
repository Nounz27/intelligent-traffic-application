from pathlib import Path
import os


# Directorios principales del proyecto.
BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BACKEND_DIR.parent
DATA_DIR = PROJECT_DIR / "data" / "processed"


class Config:
    """Configuración general de la aplicación."""

    NODES_FILE = DATA_DIR / "nodos_establecimientos_lima.csv"
    EDGES_FILE = DATA_DIR / "aristas_rutas_modeladas.csv"

    JSON_SORT_KEYS = False

    FRONTEND_ORIGIN = os.getenv(
        "FRONTEND_ORIGIN",
        "http://localhost:5173"
    )

    # Velocidad optimista utilizada por la heurística de A*.
    HEURISTIC_SPEED_KPH = 60.0

    # Peso utilizado para calcular la ruta.
    DEFAULT_WEIGHT = "tiempo_estimado_min"

    ROAD_GRAPH_FILE = (
    DATA_DIR / "red_vial_lima.graphml"
    )

    ROAD_MAPPING_FILE = (
    DATA_DIR / "establecimientos_contraste_vial.csv"
    )