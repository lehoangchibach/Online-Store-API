from .base import BaseSchema
from marshmallow import fields, ValidationError


class Password(fields.Field):
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


class UserSchema(BaseSchema):
    email = fields.Email(required=True, load_only=True)
    password = Password(required=True, load_only=True)


