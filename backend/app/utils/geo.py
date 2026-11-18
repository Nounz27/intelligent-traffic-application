import math

EARTH_RADIUS_KM = 6371.0

def haversine_km(
    latitude_a: float,
    longitude_a: float,
    latitude_b: float,
    longitude_b: float
) -> float:
    """
    Calcula la distancia en línea recta entre dos coordenadas.

    Retorna la distancia en kilómetros.
    """

    lat_a = math.radians(latitude_a)
    lon_a = math.radians(longitude_a)

    lat_b = math.radians(latitude_b)
    lon_b = math.radians(longitude_b)

    delta_lat = lat_b - lat_a
    delta_lon = lon_b - lon_a

    value = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat_a)
        * math.cos(lat_b)
        * math.sin(delta_lon / 2) ** 2
    )

    central_angle = 2 * math.atan2(
        math.sqrt(value),
        math.sqrt(1 - value)
    )

    return EARTH_RADIUS_KM * central_angle