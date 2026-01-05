import requests
from typing import Tuple, List

Coordinate = Tuple[float, float]

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
    
    def _post(self, query_url: str, data: dict) -> dict:
        url = f"{self.base_url}/{query_url}"
        response = requests.post(url, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def _validate_profile(self, profile: str):
        valid_profiles = ["driving-car", "foot-walking"]
        if not profile in valid_profiles:
            raise ValueError(f"Invalid profile: {profile}")

    def simple_path(self, coordinates: List[Coordinate]) -> dict:
        data = {
            "coordinates": coordinates,
        }
        return self._post(f"v2/directions/{self.profile}", data)
    
    def matrix_s2d(self, sources: List[Coordinate], destinations: List[Coordinate], metrics : List[str] = None) -> dict:
        if metrics is None:
            metrics = [self.default_metric]
        locations = sources + destinations
        sources_indices = list(range(len(sources)))
        destinations_indices = list(range(len(sources), len(sources) + len(destinations)))
        data = {
            "locations": locations,
            "destinations": destinations_indices,
            "metrics": metrics,
            "sources": sources_indices
        }
        return self._post(f"v2/matrix/{self.profile}", data)
    
    def matrix(self, coordinates: List[Coordinate], metrics : List[str] = None) -> dict:
        if metrics is None:
            metrics = [self.default_metric]
        data = {
            "locations": coordinates,
            "metrics": metrics
        }
        return self._post(f"v2/matrix/{self.profile}", data)
    
    def isochrones(self, coordinates: Coordinate, range: List[int], range_type: str = None, intersections: bool = False) -> dict:
        data = {
            "locations": [coordinates],
            "range": range,
        }
        if range_type:
            data["range_type"] = range_type
        if intersections:
            data["intersections"] = True
        return self._post(f"v2/isochrones/{self.profile}", data)