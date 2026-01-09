from typing import Tuple, List

Coordinate = Tuple[float, float] # (lat, lng)

# Standdard of the app states coordinates as (lat, lng)
# but ORS API and Map Client use (lng, lat)
def reverse_coordinates(coordinate: Coordinate) -> Coordinate:
    return (coordinate[1], coordinate[0])
def reverse_coordinates_list(coordinates: List[Coordinate]) -> List[Coordinate]:
    return [(coord[1], coord[0]) for coord in coordinates]