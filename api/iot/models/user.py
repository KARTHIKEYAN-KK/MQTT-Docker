from email.policy import default
from db import db
import datetime


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(256), unique=True)
    phoneNumber = db.Column(db.String(256), unique=True)
    role = db.Column(db.Integer, default=1)
    password = db.Column(db.String(256), unique=False)
    status = db.Column(db.Boolean, default=False)
    added_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
