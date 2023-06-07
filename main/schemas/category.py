from marshmallow import fields

from .base import BaseSchema, NameField, PaginationSchema


class CategorySchema(BaseSchema):
    id = fields.Integer(required=True, dump_only=True)
    name = NameField(required=True)
    is_creator = fields.Boolean(required=True, dump_only=True)


class CategoriesSchema(PaginationSchema):
    categories = fields.List(fields.Nested(CategorySchema()), dump_only=True)
