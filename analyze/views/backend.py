import subprocess
import json

import sys
import os

dlSystemDir = os.getenv('DL_SYSTEM_PATH')
if dlSystemDir is not None:
    sys.path.append("%s/rpc_server/config" % dlSystemDir)
else:
    print("please set DL_SYSTEM_PATH")
    sys.exit()

from config_parser import device_parser, backend_parser


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
    backends = backend_parser()
    backends = json.loads(backends)
    return backends

def check_devices():
    devices = device_parser()
    devices = json.loads(devices)

    for device in devices:
        print(device)

        device['status'] = is_device_online(device['number'])
    return devices
