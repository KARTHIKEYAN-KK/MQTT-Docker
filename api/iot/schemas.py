from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    phoneNumber = fields.Str(required=True)
    role = fields.Int(dump_only=True)
    password = fields.Str(required=True, load_only=True)
    status = fields.Bool(dump_only=True)
    added_date = fields.DateTime(dump_only=True)

class UserLoginSchema(Schema):
    phoneNumber = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class UserDetailsSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    phoneNumber = fields.Str(required=True)

class DeviceDataSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    mac_address = fields.Str(required=True)
    city_name = fields.Str(required=True)
    state_name = fields.Str(required=True)
    bridge_name = fields.Str(required=True)
    lattitude = fields.Str(required=True)
    lontitude = fields.Str(required=True)
    added_date = fields.Str(required=True)
    status = fields.Boolean(required=True)
    flood_status = fields.Boolean(required=True)
    gsm_signal = fields.Str(required=True)
    flood_count = fields.Str(required=True)
    last_updated = fields.Str(required=True)