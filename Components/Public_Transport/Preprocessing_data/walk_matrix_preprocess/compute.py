from Components.Map_Service import ORSClient
import time
import json
from contextlib import contextmanager

def compute_walk_matrix(stop_data):
    ors_client_walk = ORSClient("foot-walking")
    coordinates = []
    for stop in stop_data['stops']:
        coordinates.append((stop['lat'], stop['lng']))
    walk_matrix = [[0.0]]
    for i in range(1, stop_data['number_of_stops'] + 1):
        current_stop = (stop_data['stops'][i]['lat'], stop_data['stops'][i]['lng'])
        coordinates[0] = current_stop
        walk_matrix_response = ors_client_walk.matrix_s2d([current_stop], coordinates)
        walk_matrix.append(walk_matrix_response['distances'][0])
        print(f"Computed walk distances from stop {i}/{stop_data['number_of_stops']}", flush=True)
    return walk_matrix