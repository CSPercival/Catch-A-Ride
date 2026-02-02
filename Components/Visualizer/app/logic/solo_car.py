from flask import Blueprint, render_template, jsonify, request, current_app
from Components.Map_Service.mapors_getters import single_geometry
from Components.Visualizer.app.logic.map_orders import MapOrders

# Create the blueprint
solo_car_bp = Blueprint('solo_car_bp', __name__)

@solo_car_bp.route('/car')
def show_site():
    return render_template('tmp4.html')

@solo_car_bp.route('/car/computing', methods=["POST"])
def compute_routes():
    print("hello from python")
    input_form = request.get_json()
    start_address = input_form['carStartAddress']
    finish_address = input_form['finishAddress']
    if not start_address['valid'] or not finish_address['valid']:
        return jsonify(valid=False, message="Invalid addresses")
    geo_results = current_app.ors_client_drive.simple_path([[start_address['lat'], start_address['lng']], [finish_address['lat'], finish_address['lng']]])
    map_orders = MapOrders()
    # map_orders = {
    #     "clearCommonLandmarks" : True,
    #     "clearPolylines": True,
    #     "landmarksToAdd" : [],
    #     "polylinesToAdd" : [
    #         {
    #             "geometry": single_geometry(geo_results),
    #             "options": {
    #                 "color": "blue",
    #             },
    #             "popupContent": "Car route from " + start_address['name'] + " to " + finish_address['name']
    #         }        
    #     ]
    # }
    map_orders.clear_orders()
    map_orders.add_car(geo_results, "Car route from " + start_address['name'] + " to " + finish_address['name'])
    return map_orders.get_orders()
    
