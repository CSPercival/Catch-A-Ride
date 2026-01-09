from flask import Flask
# from Map_Service.ors_client import ORSClient
# from ...Map_Service.map_client import MapClient
from Components.Map_Service import ORSClient
from Components.Map_Service import MapClient


def create_app():
    app = Flask(__name__)

    from .logic.home import home_bp
    from .logic.solo_car import solo_car_bp
    from .logic.input_validator import input_validator_bp
    # from .routes.maps import map_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(solo_car_bp)
    app.register_blueprint(input_validator_bp)
    # app.register_blueprint(map_bp)

    app.ors_client_walk = ORSClient("foot-walking")
    app.ors_client_drive = ORSClient("driving-car")
    app.map_client = MapClient()

    return app