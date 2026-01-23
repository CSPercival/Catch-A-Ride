from flask import Flask, current_app
from Components.Map_Service import ORSClient
from Components.Map_Service import MapClient
from Components.Public_Transport.Client.pt_client import PTClient
from Components.Meeting_Point_Service.client import MPSClient
# from Components.Visualizer.app.logic.order_creator import MapOrders

def create_app():
    app = Flask(__name__)

    from .logic.home import home_bp
    from .logic.solo_car import solo_car_bp
    from .logic.duo import duo_bp
    from .logic.input_validator import input_validator_bp
    # from .routes.maps import map_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(solo_car_bp)
    app.register_blueprint(duo_bp)
    app.register_blueprint(input_validator_bp)
    # app.register_blueprint(map_bp)

    ors_client_walk = ORSClient("foot-walking")
    ors_client_drive = ORSClient("driving-car")
    map_client = MapClient()
    pt_client = PTClient(0, "XD", ors_client_walk)
    mps_client = MPSClient(ors_client_walk, ors_client_drive, 
                               map_client, pt_client)

    app.ors_client_walk = ors_client_walk
    app.ors_client_drive = ors_client_drive
    app.map_client = map_client
    app.pt_client = pt_client
    app.mps_client = mps_client
    # app.map_orders = MapOrders()
    return app