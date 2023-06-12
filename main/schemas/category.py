from marshmallow import fields, pre_load
from marshmallow.validate import Length

from .base import BaseSchema, PaginationSchema


class CategoryCreateSchema(BaseSchema):
    name = fields.String(required=True, validate=Length(min=1, max=255))

    # Clean up data
    @pre_load
    def process_input(self, data, **__):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data


class CategorySchema(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    is_creator = fields.Boolean()


class CategoriesSchema(PaginationSchema):
    categories = fields.List(fields.Nested(CategorySchema()))
