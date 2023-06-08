from .base import BaseSchema, PasswordField
from marshmallow import fields


class UserLoadSchema(BaseSchema):
    email = fields.Email(required=True, load_only=True)
    password = PasswordField(required=True, load_only=True)
