from flask import Flask

def create_app():
    app = Flask(__name__)

    from .logic.home import home_bp
    from .logic.solo_car import solo_car_bp
    # from .routes.maps import map_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(solo_car_bp)
    # app.register_blueprint(map_bp)

    return app