import json
import os
import sys
from pathlib import Path

current_path = Path(__file__).resolve().parent
device_json_path = os.path.join(current_path, "config_device.json")
setup_json_path = os.path.join(current_path, "config_sdk.json")

def device_parser():
    with open(device_json_path, "r") as file:
        data = json.load(file)

    transformed_data = []
    for key, values in data.items():
        for value in values:
            transformed_data.append({
                "name": f"{key}",
                "number": f"{value}",
                "status": False
            })

    return json.dumps(transformed_data, indent=2)


def backend_parser():
    with open(setup_json_path, "r") as file:
        data = json.load(file)

    transformed_data = {key: list(values.keys()) for key, values in data.items()}
    
    return json.dumps(transformed_data, indent=2)

