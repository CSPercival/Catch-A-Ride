import requests
import json
from shapely.geometry import shape, Point
from typing import Tuple, List

Coordinate = Tuple[float, float]

class MapClient:
    def __init__(self, api_key: str = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjIzMjIxM2Q3YWY4ZjQzMGRhZjY4NTJmNzM3NTI3YTM2IiwiaCI6Im11cm11cjY0In0=", timeout: int = 60):
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = "https://api.openrouteservice.org/geocode"
        self.headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
            'Authorization': self.api_key
        }
        with open('./Components/Map_Service/data/map_boundaries.geojson') as f:
            self.map_boundaries = json.load(f)
        self.map_polygon = shape(self.map_boundaries['features'][0]['geometry'])
    
    def _get(self, query_url: str, data: dict) -> dict:
        url = f"{self.base_url}/{query_url}"
        response = requests.get(url, headers=self.headers, params=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def geocode(self, text: str) -> dict:
        data = {
            "text": text,
            "boundary.country": 'PL',
            "focus.point.lon": 17.0385,
            "focus.point.lat": 51.1079,
        }
        return self._get("search", data)
    
    def reverse_geocode(self, coordinates: Coordinate) -> dict:
        data = {
            "point.lon": coordinates[0],
            "point.lat": coordinates[1],
            "boundary.country": 'PL',
            "focus.point.lon": 17.0385,
            "focus.point.lat": 51.1079,
        }
        return self._get("reverse", data)
    
    def validate_coordinates(self, coordiante : Coordinate):
        point = Point(coordiante[0], coordiante[1])
        return self.map_polygon.contains(point)