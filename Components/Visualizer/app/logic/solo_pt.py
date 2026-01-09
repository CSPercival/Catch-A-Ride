from flask import Blueprint, render_template, jsonify

# Create the blueprint
home_bp = Blueprint('home_bp', __name__)

@home_bp.logic('/home')
def option1():
    return render_template('home.html')