from email.policy import default
from db import db
import datetime


class DeviceDataModel(db.Model):
    __tablename__ = "devicedata"

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"))
    mac_address = db.Column(db.String(80), db.ForeignKey("device.mac_address"))
    gsm_signal = db.Column(db.String(10))
    flood_status = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)