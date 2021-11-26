from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    
class AuthUserSchema(Schema):
    username = fields.String(required = True, error_messages={"required": "Username is required"})
    password = fields.String(required = True, error_messages={"required": "Password is required"})
    

class UpdateUserSchema(Schema):
    username = fields.String(missing=None)
    password = fields.String(missing=None)
