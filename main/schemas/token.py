from marshmallow import fields

from .base import BaseSchema


class TokenDumpSchema(BaseSchema):
    access_token = fields.String()
