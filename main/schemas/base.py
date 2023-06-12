from flask import jsonify, request
from marshmallow import EXCLUDE, Schema, ValidationError, fields, pre_load
from marshmallow.validate import Range


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))

    @pre_load
    def process_input(self, data, **__):
        if request.method == "GET":
            return data
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = value.strip()
        return data


class PaginationSchema(BaseSchema):
    items_per_page = fields.Integer(load_default=20, validate=Range(min=1))
    page = fields.Integer(load_default=1, validate=Range(min=1))
    total_items = fields.Integer()


class PasswordField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, str):
            raise ValidationError("Password must be a string.")
        value = value.strip()
        if len(value) < 6 or len(value) > 30:
            raise ValidationError("Length of password must in range 6-30.")

        contain_upper, contain_lower, contain_digit = False, False, False
        for i in value:
            if i.isupper():
                contain_upper = True
            if i.islower():
                contain_lower = True
            if i.isdigit():
                contain_digit = True

        if not (contain_upper and contain_lower and contain_digit):
            raise ValidationError("Password does not meet constraints.")

        return value
