from flask import Flask
from flask_smorest import Api
from flask_cors import CORS

from resources.hindu_tamil import blp as HinduTamilTamilnaduBlueprint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "FUEL PRICE API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/help"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["CORS_HEADERS"] = set()

api = Api(app)
CORS(app)  # Enable CORS for all routes

api.register_blueprint(HinduTamilTamilnaduBlueprint)

# Enable CORS
@app.before_request
def before_request():
    # Allow requests from all origins
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }
    for key, value in headers.items():
        app.config["CORS_HEADERS"].add(key)