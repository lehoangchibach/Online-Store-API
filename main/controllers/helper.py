from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest as InvalidJsonBody

from main.commons.exceptions import BadRequest


def load_json(schema, request):
    try:
        if request.method == "GET":
            data = schema.load(request.args)
        else:
            data = schema.load(request.get_json())
    except ValidationError as e:
        # validate email address and password
        raise BadRequest(error_data=e.messages)
    except InvalidJsonBody:
        # check request with no body
        raise BadRequest(error_message="Request's body is not a json.")
    return data


def validate_id(object_id, if_field_name):
    try:
        object_id = int(object_id)
    except ValueError:
        # validate id
        raise BadRequest(error_data={if_field_name: ["Id is not an integer."]})
    if object_id < 0:
        raise BadRequest(
            error_data={if_field_name: ["Id can not be a negative integer."]}
        )
    return object_id


def get_ownership_item(item, user_id):
    result = dict()
    for key, value in item.__dict__.items():
        if key == "creator_id":
            result["is_creator"] = user_id == value
        else:
            result[key] = value
    return result


def get_ownership_list_items(items, user_id):
    return [get_ownership_item(item, user_id) for item in items]
