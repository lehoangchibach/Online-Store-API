from .base import BaseSchema
from marshmallow import fields


class TokenSchema(BaseSchema):
    access_token = fields.String(required=True, dump_only=True)
