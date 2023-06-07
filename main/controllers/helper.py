from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest as BodyNotJson
from main.commons.exceptions import BadRequest


def load_json(schema, request):
    try:
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


def get_ownership(item, identity):
    result = dict()
    for key, value in item.__dict__.items():
        if key == "creator_id":
            result["is_creator"] = identity == value
        else:
            result[key] = value
    return result


def get_ownership_list(items, identity):
    result = []
    for item in items:
        result.append(get_ownership(item, identity))
    return result
