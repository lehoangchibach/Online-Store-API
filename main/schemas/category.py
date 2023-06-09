from marshmallow import fields, pre_load
from marshmallow.validate import Length

from .base import BaseSchema, PaginationSchema


class CategoryLoadSchema(BaseSchema):
    name = fields.String(required=True, validate=Length(min=1, max=255))

    # Clean up data
    @pre_load
    def process_input(self, data, **kwargs):
        if "name" in data and data["name"]:
            data["name"] = data["name"].lower().strip()
        return data


class CategoryDumpSchema(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    is_creator = fields.Boolean()


class CategoriesDumpSchema(PaginationSchema):
    categories = fields.List(fields.Nested(CategoryDumpSchema()))
