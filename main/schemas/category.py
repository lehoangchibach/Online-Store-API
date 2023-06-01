from .base import BaseSchema, PaginationSchema
from marshmallow import fields


class CategorySchema(BaseSchema):
    id = fields.Integer(required=True, dump_only=True)
    name = fields.String(required=True)
    is_creator = fields.Boolean(dump_only=True)


class CategoriesSchema(PaginationSchema):
    categories = fields.List(fields.Nested(CategorySchema()), dump_only=True)
