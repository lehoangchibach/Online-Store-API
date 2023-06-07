from flask import jsonify
from marshmallow import EXCLUDE, Schema, ValidationError, fields


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many=many))


class PaginationSchema(BaseSchema):
    items_per_page = fields.Integer(load_default=20, validate=lambda x: x >= 0)
    page = fields.Integer(load_default=0, validate=lambda x: x >= 0)
    total_items = fields.Integer(dump_only=True)


class NameField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, str):
            raise ValidationError("Name must be a string.")
        if len(value) == 0:
            raise ValidationError("Name must have at least 1 character.")
        value = value.strip()
        if len(value) == 0:
            raise ValidationError("Name can not contains all white-space.")
        if len(value) > 255:
            raise ValidationError("Name can not be longer than 255.")
        return value


class DescriptionField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, str):
            raise ValidationError("Description must be a string.")
        if len(value) == 0:
            raise ValidationError("Description must have at least 1 character.")
        value = value.strip()
        if len(value) == 0:
            raise ValidationError("Description can not contains all white-space.")
        if len(value) > 1024:
            raise ValidationError("Description can not be longer than 1024.")
        return value


class PasswordField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, str):
            raise ValidationError("Password must be a string.")
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
