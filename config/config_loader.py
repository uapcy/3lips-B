import yaml
import os

def load_config():
    """
    Loads configuration from config/config.yml and provides default values if missing.
    Returns:
        reference_point (dict): Contains latitude, longitude, altitude.
        time_interval (int): Time interval for velocity calculation.
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.yml")

    # Default configuration
    default_config = {
        "reference_point": {"latitude": 0, "longitude": 0, "altitude": 0},
        "default_time_interval": 5
    }

    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file) or {}  # Load YAML file, default to empty dict if None

        # Merge with defaults (ensures missing values don't cause errors)
        reference_point = config.get("reference_point", default_config["reference_point"])
        time_interval = config.get("default_time_interval", default_config["default_time_interval"])

        return reference_point, time_interval

    except FileNotFoundError:
        print(f"Warning: {config_path} not found! Using default settings.")
        return default_config["reference_point"], default_config["default_time_interval"]
