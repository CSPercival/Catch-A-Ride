import requests
from Components.Map_Service.aux_functions import reverse_coordinates, reverse_coordinates_list
from typing import Tuple, List

Coordinate = Tuple[float, float] # (lat, lng)

# TODO reverse order of returned coordinates 

# def revcoord(coords : Coordinate):
#     return [coords[1], coords[0]]

class ORSClient:
    def __init__(self, profile: str, base_url: str = "http://localhost:8085/ors", timeout: int = 60):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self._validate_profile(profile)
        self.profile = profile
        if(profile == 'driving-car'):
            self.default_metric = 'duration'
        elif(profile == 'foot-walking'):
            self.default_metric = 'distance'
    
    def _post(self, query_url: str, data: dict, check_status=True) -> dict:
        url = f"{self.base_url}/{query_url}"
        response = requests.post(url, json=data, timeout=self.timeout)
        # print(response, flush=True)
        # print(response.text, flush=True)
        if check_status:
            response.raise_for_status()
        else:
            if response.status_code != 200:
                return None
        return response.json()
    
    def _validate_profile(self, profile: str):
        valid_profiles = ["driving-car", "foot-walking"]
        if not profile in valid_profiles:
            raise ValueError(f"Invalid profile: {profile}")
        
    def _snap(self, coordinate: Coordinate, radius = 10) -> Coordinate:
        data = {
            "locations": [reverse_coordinates(coordinate)],
            "radius": radius
        }
        res = self._post(f"v2/snap/{self.profile}", data)
        print("Snap response:", res, flush=True)
        return reverse_coordinates(res['locations'][0]['location'])

    def simple_path(self, coordinates: List[Coordinate]) -> dict:
        data = {
            "coordinates": reverse_coordinates_list(coordinates),
        }
        # TODO reverse order of coordinates
        return self._post(f"v2/directions/{self.profile}", data)
    
    def matrix_s2d(self, sources: List[Coordinate], destinations: List[Coordinate], metrics : List[str] = None) -> dict:
        if metrics is None:
            metrics = [self.default_metric]
        locations = sources + destinations
        sources_indices = list(range(len(sources)))
        destinations_indices = list(range(len(sources), len(sources) + len(destinations)))
        data = {
            "locations": reverse_coordinates_list(locations),
            "destinations": destinations_indices,
            "metrics": metrics,
            "sources": sources_indices
        }
        # TODO reverse order of coordinates
        return self._post(f"v2/matrix/{self.profile}", data)
    
    def matrix(self, coordinates: List[Coordinate], metrics : List[str] = None) -> dict:
        if metrics is None:
            metrics = [self.default_metric]
        data = {
            "locations": reverse_coordinates_list(coordinates),
            "metrics": metrics
        }
        # TODO reverse order of coordinates
        return self._post(f"v2/matrix/{self.profile}", data)
    
    def isochrones(self, coordinates: List[Coordinate], range: List[int], range_type: str = None, intersections: bool = False, interval: int = None) -> dict:
        # coordinates = [self._snap(coords) for coords in coordinates]
        # print("coords after snapping:", coordinates)
        data = {
            "locations": reverse_coordinates_list(coordinates),
            "range": range,
        }
        if range_type:
            data["range_type"] = range_type
        if intersections:
            data["intersections"] = "true"
        if interval:
            data["interval"] = interval
        # TODO reverse order of coordinates
        return self._post(f"v2/isochrones/{self.profile}", data)
    
    def _isochrones_to_geometries(self, coordinate: Coordinate, isochrones_responses: List[dict], limit: int) -> dict:
        geometries = [[] for _ in range(limit + 1)]
        geometries[0] = [coordinate]
        for isochrone_response in isochrones_responses:
            if isochrone_response == None:
                continue
            for feature in isochrone_response["features"]:
                dist = int(feature["properties"]["value"]) // 60
                coordinates = reverse_coordinates_list(feature["geometry"]["coordinates"][0])
                geometries[dist] = coordinates
        for i in range(1, limit + 1):
            if len(geometries[i]) == 0:
                geometries[i] = geometries[i - 1]
        return geometries

    def range_isochrones_geometries(self, coordinate: Coordinate, max_range: int = 3600, interval: int = 60, smoothing: float = -1.0) -> dict:
        data = {
            "locations": reverse_coordinates_list([coordinate]),
            "range": [max_range],
            "interval": interval
        }
        if smoothing != -1.0:
            data["smoothing"] = smoothing
        print("Trying: ", coordinate, flush=True)
        response = self._post(f"v2/isochrones/{self.profile}", data, check_status=False)
        if response is not None:
            return self._isochrones_to_geometries(coordinate, [response], max_range // interval)
        
        coordinate = self._snap(coordinate)
        data["locations"] = reverse_coordinates_list([coordinate])
        print("Trying with snapping: ", coordinate, flush=True)
        response = self._post(f"v2/isochrones/{self.profile}", data, check_status=False)
        if response is not None:
            return self._isochrones_to_geometries(coordinate, [response], max_range // interval)
        print("Failed", flush=True)

        del data["interval"]
        isochrones_responses = []
        for dist in range(interval, max_range + interval, interval):
            data["range"] = [dist]
            response = self._post(f"v2/isochrones/{self.profile}", data, check_status=False)
            isochrones_responses.append(response)
        return self._isochrones_to_geometries(coordinate, isochrones_responses, max_range // interval)