from email.policy import default
from db import db
import datetime


class DeviceModel(db.Model):
    __tablename__ = "device"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    mac_address = db.Column(db.String(80), unique=True, index=True)
    city_name = db.Column(db.String(80))
    state_name = db.Column(db.String(80))
    bridge_name = db.Column(db.String(100))
    lattitude = db.Column(db.String(15))
    lontitude = db.Column(db.String(15))
    added_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.Boolean, default=False)
    flood_status = db.Column(db.Boolean, default=False)
    gsm_signal = gsm_signal = db.Column(db.String(10))
    flood_count = db.Column(db.String(10))
    last_updated = db.Column(db.String(1000))
