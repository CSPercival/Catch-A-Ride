# from flask import Blueprint, render_template
from flask import Blueprint, request, jsonify
# Create the blueprint
input_validator_bp = Blueprint('input_validator_bp', __name__, url_prefix='/validate')

def validate_coords(lat, lon):
    

@input_validator_bp.route("/address", methods=["POST"])
def validate_address():
    data = request.get_json()
    address = data.get("address", "")
    
    latlon = address.replace(" ", "").split(",")
    if len(latlon) == 2:
        try:
            lat = float(latlon[0])
            lon = float(latlon[1])
            return validate_coords(lat, lon)
        except ValueError:
            pass
    
    return 