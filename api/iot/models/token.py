from db import db
import datetime

class TokenModel(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    device_token = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user_id, device_token):
        self.user_id = user_id
        self.device_token = device_token

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
