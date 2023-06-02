from .base import BaseSchema, PaginationSchema, NameSchema
from marshmallow import fields


class CategorySchema(BaseSchema):
    id = fields.Integer(required=True, dump_only=True)
    name = NameSchema(required=True)
    is_creator = fields.Boolean(required=True, dump_only=True)


class CategoriesSchema(PaginationSchema):
    categories = fields.List(fields.Nested(CategorySchema()), dump_only=True)
