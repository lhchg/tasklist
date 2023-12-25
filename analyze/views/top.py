import subprocess
import json

def read_json_file(file_name):
    contents = ""
    try:
        with open(file_name, 'r') as file:
            contents = json.load(file)
    except FileNotFoundError:
        print('device.json file not found')
    except json.JSONDecodeError:
        print('Invalid JSON file')

    return contents

def is_device_online(search_string):
    output = subprocess.check_output(['adb', 'devices']).decode('utf-8')
    lines = output.split("\n")
    device_ids = [line.split()[0] for line in lines[1:] if line.strip()]
    print(device_ids)
    print(search_string)
    if search_string in device_ids:
        print(f"{search_string} is present in the device IDs.")
        result = True
    else:
        print(f"{search_string} is not in the device IDs.")
        result = False
    return result

def check_backend():
    backends = read_json_file("resource/backend.json")
    return backends

def check_devices():
    devices = read_json_file("resource/device.json")

    for device in devices:
        device['status'] = is_device_online(device['number'])
    return devices