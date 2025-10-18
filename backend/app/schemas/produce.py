from marshmallow import Schema, fields, validate

class ProduceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    description = fields.Str(required=False)
    price = fields.Decimal(as_string=True, required=True, validate=lambda p: p > 0)
    quantity = fields.Int(required=True, validate=lambda q: q >= 0)
    unit = fields.Str(required=True, validate=validate.OneOf(['kg', 'bunch', 'crate', 'item']))
    image_url = fields.URL(required=False, allow_none=True)
    is_available = fields.Bool(dump_only=True)
    location = fields.Str(required=False, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    farmer_id = fields.Int(dump_only=True)