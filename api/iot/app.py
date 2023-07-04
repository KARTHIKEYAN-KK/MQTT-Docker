from flask import Flask
from flask_smorest import Api
from db import db
from device_status import check_device_status
import models
from threading import Thread

from resources.user import blp as UserBlueprint
from resources.device import blp as DeviceBlueprint
from resources.token import blp as TokenBlueprint

def create_app(db_url=None):

    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "FUEL PRICE API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/help"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        db_url 
        or "postgresql://postgres:postgres@13.232.49.108:5001/iot"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(DeviceBlueprint)
    api.register_blueprint(TokenBlueprint)

    thread = Thread(target=check_device_status, args=(app,))
    thread.start()

    return app