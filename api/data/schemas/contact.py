from marshmallow import Schema, fields


class ContactSchema(Schema):
    id      = fields.Int()
    user_id = fields.Int()
    name    = fields.Str(required = True, error_messages = {"required": "name is a required field"})
    phone   = fields.Int(required = True, error_messages = {"required": "phone is a required field"})

class UpdateContactSchema(Schema):
    name    = fields.Str(default = None)
    phone   = fields.Int(default = None)