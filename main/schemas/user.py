from marshmallow import fields

from .base import BaseSchema, PasswordField


class UserCreateSchema(BaseSchema):
    email = fields.Email(required=True, load_only=True)
    password = PasswordField(required=True, load_only=True)
