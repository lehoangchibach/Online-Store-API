from marshmallow import fields
from marshmallow.validate import Length, Range

from .base import BaseSchema, PaginationSchema


class ItemCreateSchema(BaseSchema):
    name = fields.String(required=True, validate=Length(min=1, max=255))
    description = fields.String(required=True, validate=Length(min=1, max=1024))
    category_id = fields.Integer(required=True, strict=True, validate=Range(min=0))


class ItemUpdateSchema(ItemCreateSchema):
    pass


class ItemSchema(BaseSchema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    category_id = fields.Integer()
    is_creator = fields.Boolean()


class ItemsGetManySchema(PaginationSchema):
    category_id = fields.Integer(validate=Range(min=0))


class ItemsSchema(PaginationSchema):
    items = fields.List(fields.Nested(ItemSchema()))
