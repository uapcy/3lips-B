from geopy.distance import geodesic
import math

def calculate_distance(target_coords, preset_point):
    """
    Compute the 3D distance from a target to a preset land point.
    Args:
        target_coords: (latitude, longitude, altitude)
        preset_point: (latitude, longitude, altitude)
    Returns:
        Distance in meters.
    """
    lat1, lon1, alt1 = preset_point
    lat2, lon2, alt2 = target_coords

    # Compute horizontal distance (Haversine formula)
    ground_distance = geodesic((lat1, lon1), (lat2, lon2)).meters

    # Compute vertical distance (altitude difference)
    height_difference = abs(alt2 - alt1)

    # Compute total 3D distance
    total_distance = math.sqrt(ground_distance**2 + height_difference**2)
    return total_distance
