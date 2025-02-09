from flask import Blueprint, request, jsonify
from common.ellipsoid_intersection import compute_target_position
from common.distance_calculator import calculate_distance
from common.velocity_calculator import calculate_velocity
from config.config_loader import load_config

# Create Flask Blueprint
api_bp = Blueprint('api', __name__)

# Load Configuration
PRESET_LAND_POINT, TIME_INTERVAL = load_config()
previous_targets = {}

# 📌 Route: Process target positions
@api_bp.route('/get_targets', methods=['POST'])
def get_targets():
    data = request.get_json()
    targets = []

    for target in data.get('targets', []):
        lat, lon, alt = target['lat'], target['lon'], target['alt']
        distance = calculate_distance(PRESET_LAND_POINT, (lat, lon, alt))
        
        prev_position = previous_targets.get(target['id'])
        velocity = calculate_velocity(prev_position, (lat, lon, alt), TIME_INTERVAL) if prev_position else 0
        
        previous_targets[target['id']] = (lat, lon, alt)
        
        targets.append({
            "id": target["id"],
            "lat": lat,
            "lon": lon,
            "alt": alt,
            "distance": distance,
            "velocity": velocity
        })
    
    return jsonify({"targets": targets}), 200

# Sample in-memory database for CRUD operations
data = []

# 📌 Route: Get all items (CRUD API)
@api_bp.route('/items', methods=['GET'])
def get_items():
    return jsonify({"items": data}), 200

# 📌 Route: Create a new item
@api_bp.route('/items', methods=['POST'])
def create_item():
    new_item = request.get_json()
    new_item["id"] = len(data) + 1
    data.append(new_item)
    return jsonify(new_item), 201

# 📌 Route: Update an item
@api_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in data if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    item.update(request.get_json())
    return jsonify(item), 200

# 📌 Route: Delete an item
@api_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global data
    data = [item for item in data if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200
