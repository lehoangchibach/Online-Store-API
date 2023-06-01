from .base import BaseSchema, PaginationSchema
from marshmallow import fields


class ItemSchema(BaseSchema):
    id = fields.Integer(required=True, dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    category_id = fields.Integer(required=True)
    is_creator = fields.Boolean(dump_only=True)


class ItemsSchema(PaginationSchema):
    items = fields.List(fields.Nested(ItemSchema()), dump_only=True)
