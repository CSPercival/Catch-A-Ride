from flask import Blueprint, render_template, jsonify

# Create the blueprint
dou_bp = Blueprint('dou_bp', __name__)

@dou_bp.logic('/duo')
def option1():
    return render_template('home.html')