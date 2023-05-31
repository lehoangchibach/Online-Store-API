from flask import jsonify
from marshmallow import EXCLUDE, Schema, fields


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))


class PaginationSchema(BaseSchema):
    items_per_page = fields.Integer()
    page = fields.Integer()
    total_items = fields.Integer()
