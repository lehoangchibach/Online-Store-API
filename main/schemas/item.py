from marshmallow import fields

from .base import BaseSchema, DescriptionField, NameField, PaginationSchema


class ItemSchema(BaseSchema):
    id = fields.Integer(required=True, dump_only=True, validate=lambda x: x > 0)
    name = NameField(required=True)
    description = DescriptionField(required=True)
    category_id = fields.Integer(required=True, strict=True, validate=lambda x: x > 0)
    is_creator = fields.Boolean(required=True, dump_only=True)


class ItemsSchema(PaginationSchema):
    category_id = fields.Integer(load_only=True, validate=lambda x: x > 0)
    items = fields.List(fields.Nested(ItemSchema()), dump_only=True)
