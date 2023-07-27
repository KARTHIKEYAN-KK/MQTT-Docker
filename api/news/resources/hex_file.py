from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import json, request
from schemas import EspDataSchema
import requests

blp = Blueprint("Hex file API", __name__, description="")

def fetch_hex_file(url):
    response = requests.get(url)
    return response.text

@blp.route("/download/frimware")
class FrimwareFile(MethodView):
    def get(self):
        file_url = request.args.get('url')
        if file_url:
            hex_data = fetch_hex_file(file_url)
            return hex_data
        else:
            return {"message":"Please provide the url parameter."},400


@blp.route("/esp/data")

class DataForTesting(MethodView):
    data = {
        "data": "start#SuperZIG23#4#false#104#90#true#true"
        }

    def get(self):
        return self.data

    @blp.arguments(EspDataSchema)
    def put(self, data):
        try:
            updated_data = request.json
            self.data.update(updated_data)

            return {"message": "Data updated successfully."}, 200

        except Exception as e:
            print("Error:", e)
            return {"message": "error {e}"}, 500