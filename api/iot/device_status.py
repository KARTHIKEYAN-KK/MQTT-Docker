from models.device import DeviceModel
from models.devicedata import DeviceDataModel
from models.token import TokenModel
from db import db

import time
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from flask import request

# Initialize Firebase Admin SDK
cred = credentials.Certificate("./Servicekey.json")
firebase_admin.initialize_app(cred)

def send_firebase_notification(device_token):
    message = messaging.Message(
        notification=messaging.Notification(
            title="Flood Alert",
            body="Flood detected on your device!"
        ),
        token=device_token
    )
    response = messaging.send(message)
    print("Firebase Notification sent:", response)


def check_device_status(app):
    while True:
        with app.app_context():
            devices = DeviceModel.query.all()

            for device in devices:
                device_data = DeviceDataModel.query.filter_by(device_id=device.id).order_by(DeviceDataModel.timestamp.desc()).first()
                if device_data:
                    device.flood_status = device_data.flood_status
                    device.gsm_signal = device_data.gsm_signal
                    device.last_updated = device_data.timestamp

                    # Calculate distinct flood days
                    distinct_flood_days = set()
                    device_data_entries = DeviceDataModel.query.filter_by(device_id=device.id, flood_status=True).all()
                    for entry in device_data_entries:
                        datetime_obj = entry.timestamp
                        day = datetime_obj.strftime('%Y-%m-%d')
                        distinct_flood_days.add(day)

                    # Update the flood count for the device
                    device.flood_count = len(distinct_flood_days)

            # # Get all the device tokens from the TokenModel
            # token_entries = TokenModel.query.all()
            # for token_entry in token_entries:
            #     device_token = token_entry.device_token
            #     # Send Firebase notification if flood status is true
            #     if device.flood_status:
            #         send_firebase_notification(device_token)

            # Update device status
            if device_data is not None:
                timestamp_str = device_data.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                time_difference = datetime.utcnow() - timestamp

                if time_difference.total_seconds() > 15:
                    device.status = False
                else:
                    if device.status == False:
                        device.status = True

            db.session.commit()

            time.sleep(5)
