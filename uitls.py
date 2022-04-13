import math
import httpx

MAP_BOX = "pk.eyJ1Ijoic2lzb2x1c21heGltdXMiLCJhIjoiY2wxeGYwaDFxMDI3dzNpbXg2MmRic2drbSJ9.g93acC4lMNaOvTCRuVoq0A"


def calculate_distance(point1: [float, float], point2: [float, float]) -> int:
    """
    Implements Haversine formula to calculate distance between two points.
        a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
        c = 2 ⋅ atan2( √a, √(1−a) )
        d = R ⋅ c
        φ is latitude, λ is longitude, R is earth’s mean radius = 6,371km;
        Angles need to be in radians to be acceptable by trig functions.

    :param point1: long and lat of first point
    :param point2: long and lat of second point
    :return: Distance between points in kilometers as integer
    """
    r = 6371e3  # meters
    phi1 = point1[1] * math.pi / 180
    phi2 = point2[1] * math.pi / 180
    delta_phi = (point2[1] - point1[1]) * math.pi / 180
    delta_lambda = (point2[0] - point1[0]) * math.pi / 180

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return int((r * c) / 1000)


def get_coordinates(from_: str, to_: str):
    from_coors = httpx.get(
        f"https://api.mapbox.com/geocoding/v5/mapbox.places/{from_}.json?limit=1&access_token={MAP_BOX}"
    ).json()
    from_coors = from_coors['features'][0]["geometry"]["coordinates"]
    to_coors = httpx.get(
        f"https://api.mapbox.com/geocoding/v5/mapbox.places/{to_}.json?limit=1&access_token={MAP_BOX}"
    ).json()
    to_coors = to_coors['features'][0]["geometry"]["coordinates"]
    return from_coors, to_coors
