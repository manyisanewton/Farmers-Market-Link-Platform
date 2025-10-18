# app/schemas/order.py
from marshmallow import Schema, fields, validate
from .produce import ProduceSchema

class OrderItemSchema(Schema):
    # For input validation when creating an order
    produce_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=lambda q: q > 0)

class OrderItemResponseSchema(Schema):
    # For serializing order item details in a response
    quantity = fields.Int()
    price_per_unit = fields.Decimal(as_string=True)
    produce = fields.Nested(ProduceSchema, only=("id", "name", "unit"))

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    buyer_id = fields.Int(dump_only=True)
    status = fields.Str(dump_only=True)
    total_price = fields.Decimal(as_string=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    
    # Use 'items' for input, which will contain a list of produce_id and quantity
    items = fields.List(fields.Nested(OrderItemSchema), required=True, load_only=True)

    # Use 'order_items' for output, which will have more detailed information
    order_items = fields.List(fields.Nested(OrderItemResponseSchema), attribute="items", dump_only=True)