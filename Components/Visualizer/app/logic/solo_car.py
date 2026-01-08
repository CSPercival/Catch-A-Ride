from flask import Blueprint, render_template, jsonify, request

# Create the blueprint
solo_car_bp = Blueprint('solo_car_bp', __name__)

@solo_car_bp.route('/car')
def show_site():
    return render_template('solo_car.html')

@solo_car_bp.route('/car/computing', methods=["POST"])
def compute_routes():
    input_form = request.get_json()
    print("hello from python")
    print(input_form)
    return jsonify(valid=True)
    
