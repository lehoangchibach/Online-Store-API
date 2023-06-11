from typing import Any, Dict

from flask import Request
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest as InvalidJsonBody

from main.commons.exceptions import BadRequest
from main.schemas.base import BaseSchema


def load_json(schema: BaseSchema, request: Request) -> Dict[str, Any]:
    try:
        if request.method == "GET":
            data = schema.load(request.args)
        else:
            data = schema.load(request.get_json())
    except ValidationError as e:
        raise BadRequest(error_data=e.messages)
    except InvalidJsonBody:
        # check request with invalid json body
        raise BadRequest(error_message="Request's body is not a valid json.")
    return data
