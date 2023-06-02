from .base import BaseSchema, PasswordSchema
from marshmallow import fields



class UserSchema(BaseSchema):
    email = fields.Email(required=True, load_only=True)
    password = PasswordSchema(required=True, load_only=True)


