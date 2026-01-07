from flask import Blueprint, render_template, jsonify

# Create the blueprint
solo_car_bp = Blueprint('solo_car_bp', __name__)

@solo_car_bp.route('/car')
def show_site():
    return render_template('solo_car.html')