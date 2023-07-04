from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import json, request

from db import db
from models import TokenModel

blp = Blueprint("Token", "token", description="Token data")

@blp.route("/token/<string:user_id>")
class UpdateToken(MethodView):
    def post(self, user_id):
        device_token = request.args.get("token")
        token_entry = TokenModel.query.filter_by(user_id=user_id).first()

        if token_entry:
            token_entry.device_token = device_token
        else:
            token_entry = TokenModel(user_id=user_id, device_token=device_token)
            db.session.add(token_entry)

        db.session.commit()

        return {
                    "message": "Token updated"
                }, 200
