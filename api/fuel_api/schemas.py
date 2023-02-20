from marshmallow import Schema, fields

class FuelPriceSchema(Schema):
    petrol = fields.Str()
    diesel = fields.Str()

class CityFuelPricesSchema(Schema):
    city = fields.Str()
    petrol = fields.Str()
    diesel = fields.Str()

class AllCityFuelPricesSchema(Schema):
    city = fields.Nested(FuelPriceSchema)