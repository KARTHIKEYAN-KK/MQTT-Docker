from marshmallow import Schema, fields

class DataSchema(Schema):
    time = fields.Str(dump_only=True)
    v1 = fields.Str(required=True)
    v2 = fields.Str(required=True)
    v3 = fields.Str(required=True)

    
class DataUpdateSchema(Schema):
    v1 = fields.Str()
    v2 = fields.Str()
    v3 = fields.Str()

# class FuelPriceSchema(Schema):
#     petrol = fields.Str()
#     diesel = fields.Str()

# class CityFuelPricesSchema(Schema):
#     city = fields.Str()
#     petrol = fields.Str()
#     diesel = fields.Str()

# class AllCityFuelPricesSchema(Schema):
#     city = fields.Nested(FuelPriceSchema)