import json
import os

from src.surface.surfaces import RESOURCE_DIR

_MAP_DATA = {}


def load_map(map_name):
    if map_name not in _MAP_DATA:
        file_path = os.path.join(RESOURCE_DIR, "map", map_name)
        with open(file_path, 'r') as f:
            _MAP_DATA[map_name] = json.load(f)
    map_data = _MAP_DATA[map_name]
    layers = []
    for layer in map_data["layers"]:
        layers.append(layer)
    return layers
