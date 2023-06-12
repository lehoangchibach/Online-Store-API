from marshmallow import fields

from .base import BaseSchema
from .user import UserCreateSchema


class TokenLoginSchema(UserCreateSchema):
    pass


class TokenSchema(BaseSchema):
    access_token = fields.String()
