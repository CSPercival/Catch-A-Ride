from flask import Flask, current_app
from Components.Map_Service import ORSClient
from Components.Map_Service import MapClient
from Components.Public_Transport.Client.pt_client import PTClient
from Components.Meeting_Point_Service.client import MPSClient

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
    app.pt_client = PTClient(0, "XD", current_app.ors_client_walk)
    app.mps_client = MPSClient(current_app.ors_client_walk, current_app.ors_client_drive, 
                               current_app.map_client, current_app.pt_client)
    return app