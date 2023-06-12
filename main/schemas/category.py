from marshmallow import fields
from marshmallow.validate import Length

from .base import BaseSchema, PaginationSchema


class CategoryCreateSchema(BaseSchema):
    name = fields.String(required=True, validate=Length(min=1, max=255))


class CategorySchema(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    is_creator = fields.Boolean()


class CategoriesSchema(PaginationSchema):
    categories = fields.List(fields.Nested(CategorySchema()))
