from marshmallow import fields

from .base import BaseSchema, PasswordField


class TokenLoginSchema(BaseSchema):
    email = fields.Email(required=True, load_only=True)
    password = PasswordField(required=True, load_only=True)


class TokenSchema(BaseSchema):
    access_token = fields.String()
