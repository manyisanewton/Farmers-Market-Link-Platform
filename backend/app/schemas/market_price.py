# app/schemas/market_price.py
from marshmallow import Schema, fields, validate

class MarketPriceSchema(Schema):
    id = fields.Int(dump_only=True)
    crop_name = fields.Str(required=True, validate=validate.Length(min=2))
    average_price = fields.Decimal(as_string=True, required=True, validate=lambda p: p > 0)
    unit = fields.Str(required=True)
    last_updated = fields.DateTime(dump_only=True)
