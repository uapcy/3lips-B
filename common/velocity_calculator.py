from geopy.distance import geodesic
import math

def calculate_velocity(prev_position, current_position, time_interval):
    """
    Compute velocity based on the change in position over time.
    Args:
        prev_position: (latitude, longitude, altitude) at time T1
        current_position: (latitude, longitude, altitude) at time T2
        time_interval: Time difference in seconds between T1 and T2
    Returns:
        Velocity in meters per second (m/s)
    """
    if prev_position is None:
        return 0  # If no previous data, velocity is unknown

    lat1, lon1, alt1 = prev_position
    lat2, lon2, alt2 = current_position

    # Compute horizontal distance
    ground_distance = geodesic((lat1, lon1), (lat2, lon2)).meters

    # Compute vertical distance (altitude change)
    height_difference = abs(alt2 - alt1)

    # Compute total displacement
    displacement = math.sqrt(ground_distance**2 + height_difference**2)

    # Compute velocity (m/s)
    velocity = displacement / time_interval if time_interval > 0 else 0
    return velocity
