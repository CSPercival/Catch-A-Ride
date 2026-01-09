from flask import Blueprint, render_template, jsonify

# Create the blueprint
home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def show_site():
    return render_template('home.html')

# @home_bp.route('/compute-route', methods=['POST'])
# def compute():
#     # Your route calculation logic here
#     return jsonify({"path": "computed_data"})