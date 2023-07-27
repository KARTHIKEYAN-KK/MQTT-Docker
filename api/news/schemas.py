from marshmallow import Schema, fields

class EspDataSchema(Schema):
    data = fields.Str(required=True)
