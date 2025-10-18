# app/schemas/user.py
from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    phone_number = fields.Str(required=True, validate=validate.Regexp(r'^\+?1?\d{9,15}$', error="Invalid phone number format."))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    role = fields.Str(required=True, validate=validate.OneOf(['farmer', 'buyer']))
    is_approved = fields.Bool(dump_only=True)

class AdminUserUpdateSchema(Schema):
    is_approved = fields.Bool(required=True)