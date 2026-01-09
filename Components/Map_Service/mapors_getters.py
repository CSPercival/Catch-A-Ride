
def single_distance(data):
    return data["routes"][0]["summary"]["distance"]
def single_duration(data):
    return data["routes"][0]["summary"]["duration"]
def single_geometry(data):
    return data["routes"][0]["geometry"]
def matrix_distances(data):
    return data["distances"]
def matrix_durations(data):
    return data["durations"]
def isochrone_polygon(data):
    return data["features"][0]["geometry"]["coordinates"][0]
def geocode_coords(data, idx = 0):
    if len(data["features"]) <= idx:
        return None
    return data["features"][idx]["geometry"]["coordinates"]
def geocode_address(data, idx = 0):
    if len(data["features"]) <= idx:
        return None
    return data["features"][idx]["properties"]["name"]