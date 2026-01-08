from flask import Blueprint, request, current_app, jsonify
# from ....Map_Service.mapors_getters import geocode_coords, geocode_address
from Components.Map_Service.mapors_getters import geocode_coords, geocode_address

input_validator_bp = Blueprint('input_validator_bp', __name__, url_prefix='/validate')

def _validate_coords(lat, lon):
    if not current_app.map_client.validate_coordinates((lat, lon)):
        return jsonify(valid=False, message="Coordinates out of bounds")
    geo_results = current_app.map_client.reverse_geocode((lat, lon))
    good_idx = 0
    while geocode_coords(geo_results, good_idx) != None and not current_app.map_client.validate_coordinates(geocode_coords(geo_results, good_idx)):
        good_idx += 1
    if geocode_coords(geo_results, good_idx) == None:
        return jsonify(valid=False, message="Coordinates out of bounds")
    
    return jsonify(
        valid=True,
        message="Valid coordinates",
        name=geocode_address(geo_results, good_idx),
        lat=geocode_coords(geo_results, good_idx)[0],
        lon=geocode_coords(geo_results, good_idx)[1]
    )    

def _validate_address(address):
    geo_results = current_app.map_client.geocode(address)
    good_idx = 0
    while geocode_coords(geo_results, good_idx) != None and not current_app.map_client.validate_coordinates(geocode_coords(geo_results, good_idx)):
        good_idx += 1
    if geocode_coords(geo_results, good_idx) == None:
        return jsonify(valid=False, message="Place unknown or out of bounds")
    
    return jsonify(
        valid=True,
        message="Valid place",
        name=geocode_address(geo_results, good_idx),
        lat=geocode_coords(geo_results, good_idx)[0],
        lon=geocode_coords(geo_results, good_idx)[1]
    )


@input_validator_bp.route("/address", methods=["POST"])
def validate_address():
    data = request.get_json()
    address = data.get("address", "")
    
    if address == "":
        return jsonify(valid=False, message="Empty field")
    
    latlon = address.replace(" ", "").split(",")
    if len(latlon) == 2:
        try:
            lat = float(latlon[0])
            lon = float(latlon[1])
            return _validate_coords(lat, lon)
        except ValueError:
            pass
    return _validate_address(address)