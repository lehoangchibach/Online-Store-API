from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest as BodyNotJson

from main.commons.exceptions import BadRequest


def load_json(schema, request, **kwargs):
    try:
        if "request_data" in kwargs:
            data = schema.load(kwargs["request_data"])
        else:
            data = schema.load(request.get_json())
    except ValidationError as e:
        # validate email address and password
        response = BadRequest()
        response.error_data = e.messages
        raise response
    except BodyNotJson:
        # check request with no body
        response = BadRequest()
        response.error_data = {}
        response.error_message = "Request's body is not a json."
        raise response
    return data


def validate_id(object_id, if_field_name):
    try:
        object_id = int(object_id)
    except ValueError:
        # validate id
        raise BadRequest(error_data={if_field_name: ["Id is not an integer."]})
    if object_id < 0:
        raise BadRequest(error_data={if_field_name: ["Id can not be a negative integer."]})
    return object_id


def get_ownership_item(item, identity):
    result = dict()
    for key, value in item.__dict__.items():
        if key == "creator_id":
            result["is_creator"] = identity == value
        else:
            result[key] = value
    return result


def get_ownership_list_item(items, identity):
    return [get_ownership_item(item, identity)
            for item in items]
