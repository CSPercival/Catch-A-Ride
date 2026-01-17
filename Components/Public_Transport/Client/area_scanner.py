from Components.Public_Transport.Client.aux_functions import get_single_stop_coords, get_stops_coords
from typing import Tuple
import math

Coordinate = Tuple[float, float] # (lat, lng)

def _distance(start: Coordinate, end: Coordinate):
    R = 6371000
    phi1 = math.radians(start[0])
    phi2 = math.radians(end[0])
    lam1 = math.radians(start[1])
    lam2 = math.radians(end[1])
    x = (lam2 - lam1) * math.cos((phi1 + phi2) / 2)
    y = (phi2 - phi1)
    return R * math.sqrt(x**2 + y**2)

def _pizza_nearest(start: Coordinate, stop_data, n_slices=24, k=4):
    ids = [i for i in range(1, stop_data['number_of_stops'] + 1)]
    coordinates = get_stops_coords(ids, stop_data).copy()
    slices = [[] for _ in range(n_slices)]
    for id, lat, lng in ids, coordinates:
        angle = math.degree(math.atan2(lat - start[0], lng - start[1]))
        slices[int(angle // (360 / n_slices))].append(id)
    
    ans = []
    for sector in slices:
        sector.sort(key=lambda id: _distance(start, get_single_stop_coords(id, stop_data)))
        for i in range(min(k, len(sector))):
            ans.append(sector[i])
    return ans

def _get_k_nearest(start: Coordinate, stop_data, k=100):
    ids = [i for i in range(1, stop_data['number_of_stops'] + 1)]
    ids.sort(key=lambda id: _distance(start, get_single_stop_coords(id, stop_data)))
    return [ids[i] for i in range(k)]

def _get_all(stop_data):
    return [i for i in range(1, stop_data['number_of_stops'] + 1)]

def stops_in_your_area(coordinate: Coordinate, stop_data):
    # return _get_all(stop_data)
    return _get_k_nearest(coordinate, stop_data, 100)