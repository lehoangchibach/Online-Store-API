from marshmallow import fields

from .base import BaseSchema, NameField, PaginationSchema


class CategoryLoadSchema(BaseSchema):
    name = NameField(required=True)


class CategoryDumpSchema(BaseSchema):
    id = fields.Integer(required=True, dump_only=True)
    name = NameField(required=True)
    is_creator = fields.Boolean(required=True, dump_only=True)


class CategoriesDumpSchema(PaginationSchema):
    categories = fields.List(fields.Nested(CategoryDumpSchema()), dump_only=True)
