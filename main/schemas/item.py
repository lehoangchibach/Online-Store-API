from marshmallow import fields, pre_load
from marshmallow.validate import Length, Range

from .base import BaseSchema, PaginationSchema


class ItemLoadSchema(BaseSchema):
    name = fields.String(required=True, validate=Length(min=1, max=255))
    description = fields.String(required=True, validate=Length(min=1, max=1024))
    category_id = fields.Integer(required=True, strict=True, validate=Range(min=0))

    # Clean up data
    @pre_load
    def process_input(self, data, **kwargs):
        if "name" in data and data["name"]:
            data["name"] = data["name"].lower().strip()
        if "description" in data and data["description"]:
            data["description"] = data["description"].lower().strip()
        return data


class ItemDumpSchema(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    category_id = fields.Integer()
    is_creator = fields.Boolean()


class ItemsLoadSchema(PaginationSchema):
    category_id = fields.Integer(validate=Range(min=0))


class ItemsDumpSchema(PaginationSchema):
    items = fields.List(fields.Nested(ItemDumpSchema()))
