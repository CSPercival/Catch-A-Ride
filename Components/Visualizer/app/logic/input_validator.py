from flask import Blueprint, request, current_app, jsonify
# from ....Map_Service.mapors_getters import geocode_coords, geocode_address
from Components.Map_Service.mapors_getters import geocode_coords, geocode_address

input_validator_bp = Blueprint('input_validator_bp', __name__, url_prefix='/validate')

def get_point_from_geo_responce(geo_responce):
    good_idx = 0
    while geocode_coords(geo_responce, good_idx) != None and not current_app.map_client.validate_coordinates(geocode_coords(geo_responce, good_idx)):
        good_idx += 1
    if geocode_coords(geo_responce, good_idx) == None:
        return None
    return {
        "name" : geocode_address(geo_responce, good_idx),
        "lat" : geocode_coords(geo_responce, good_idx)[0],
        "lng" : geocode_coords(geo_responce, good_idx)[1]
    }

def _validate_coords(lat, lng):
    if not current_app.map_client.validate_coordinates((lat, lng)):
        return jsonify(valid=False, name=lat + ", " + lng, message="Coordinates out of bounds")
    geo_results = current_app.map_client.reverse_geocode((lat, lng))
    point_info = get_point_from_geo_responce(geo_results)
    if point_info == None:
        return jsonify(valid=False, name=lat + ", " + lng, message="Coordinates out of bounds")
    return jsonify(
        valid=True,
        message="Valid place",
        name=point_info['name'],
        lat=point_info['lat'],
        lng=point_info['lng']
    )   

def _validate_address(address):
    geo_results = current_app.map_client.geocode(address)
    point_info = get_point_from_geo_responce(geo_results)
    if point_info == None:
        return jsonify(valid=False, name=address, message="Place unknown or out of bounds")
    return jsonify(
        valid=True,
        message="Valid place",
        name=point_info['name'],
        lat=point_info['lat'],
        lng=point_info['lng']
    )


@input_validator_bp.route("/address", methods=["POST"])
def validate_address():
    data = request.get_json()
    address = data.get("address", "")
    
    if address == "":
        return jsonify(valid=False, name=address, message="Empty field")
    
    latlng = address.replace(" ", "").split(",")
    if len(latlng) == 2:
        try:
            lat = float(latlng[0])
            lng = float(latlng[1])
            return _validate_coords(lat, lng)
        except ValueError:
            pass
    return _validate_address(address)