
def single_distance(data):
    return data["routes"][0]["summary"]["distance"]
def single_duration(data):
    return data["routes"][0]["summary"]["duration"]
def matrix_distances(data):
    return data["distances"]
def matrix_durations(data):
    return data["durations"]
def isochrone_polygon(data):
    return data["features"][0]["geometry"]["coordinates"][0]