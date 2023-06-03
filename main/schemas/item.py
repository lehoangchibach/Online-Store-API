from marshmallow import fields

from .base import BaseSchema, DescriptionSchema, NameSchema, PaginationSchema


class ItemSchema(BaseSchema):
    id = fields.Integer(required=True, dump_only=True)
    name = NameSchema(required=True)
    description = DescriptionSchema(required=True)
    category_id = fields.Integer(required=True)
    is_creator = fields.Boolean(required=True, dump_only=True)


class ItemsSchema(PaginationSchema):
    category_id = fields.Integer(required=True)
    items = fields.List(fields.Nested(ItemSchema()), dump_only=True)
