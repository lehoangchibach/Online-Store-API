from .base import BaseSchema
from marshmallow import fields


class TokenDumpSchema(BaseSchema):
    access_token = fields.String(required=True, dump_only=True)
