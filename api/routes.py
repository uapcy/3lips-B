from flask import Flask, jsonify, request
from common.ellipsoid_intersection import compute_target_position
from common.distance_calculator import calculate_distance
from common.velocity_calculator import calculate_velocity
from config.config_loader import load_config  # <-- Load configuration

app = Flask(__name__)

# Load reference point & time interval from config
PRESET_LAND_POINT, TIME_INTERVAL = load_config()

# Store previous positions for velocity calculation
previous_targets = {}

@app.route("/get_targets", methods=["POST"])
def get_targets():
    """
    API endpoint to get localized targets with altitude, distance, and velocity.
    """
    data = request.get_json()
    new_targets = data.get("targets", [])

    targets = []
    global previous_targets

    for i, new_target in enumerate(new_targets):
        lat, lon, alt = new_target["latitude"], new_target["longitude"], new_target["altitude"]
        distance = calculate_distance((lat, lon, alt), (PRESET_LAND_POINT["latitude"], PRESET_LAND_POINT["longitude"], PRESET_LAND_POINT["altitude"]))

        # Compute velocity
        velocity = calculate_velocity(previous_targets.get(i), (lat, lon, alt), TIME_INTERVAL)

        # Store current position for next update
        previous_targets[i] = (lat, lon, alt)

        targets.append({
            "latitude": lat,
            "longitude": lon,
            "altitude": alt,
            "distance_from_preset": distance,
            "velocity": velocity
        })

    return jsonify({"targets": targets})

if __name__ == "__main__":
    app.run(debug=True)
