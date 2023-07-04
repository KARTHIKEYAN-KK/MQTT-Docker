from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import json, request

from db import db
from models import UserModel, DeviceModel
from schemas import DeviceDataSchema

blp = Blueprint("Device", "device", description="Device data")

@blp.route("/getData/<string:user_id>")
class GetDeviceData(MethodView):
    @blp.response(200, DeviceDataSchema(many=True))
    def get(self, user_id):
        device_data = DeviceModel.query.filter(DeviceModel.user_id == user_id).all()
        if device_data:
            return device_data
        else:
            abort(401, message="No data found") 