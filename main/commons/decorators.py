from functools import wraps

from flask import request
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest as InvalidJsonBody

from main.commons.exceptions import BadRequest, NotFound
from main.db import session
from main.models.base import BaseModel
from main.schemas.base import BaseSchema


def get_by_id(model: type[BaseModel], path_variable: str):
    """
    Get an object from database by model and id (path_variable)
    """

    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            item_id = request.view_args[path_variable]
            item = session.get(model, item_id)
            if not item:
                raise NotFound(error_message=f"{path_variable.capitalize()} not found.")
            return func(item=item, *args, **kwargs)

        return decorator

    return wrapper


def get_identity(func):
    """
    Return the identity of user, None if jwt token not found
    """

    @wraps(func)
    def decorator(*args, **kwargs):
        identity = get_jwt_identity()
        return func(identity=identity, *args, **kwargs)

    return decorator


def load_json(schema: type[BaseSchema]):
    """
    Load request data through a schema
    """

    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            try:
                if request.method == "GET":
                    request_data = schema.load(request.args)
                else:
                    request_data = schema.load(request.get_json())
            except ValidationError as e:
                raise BadRequest(error_data=e.messages)
            except InvalidJsonBody:
                raise BadRequest(error_message="Request's body is not a valid json.")
            return func(request_data=request_data, *args, **kwargs)

        return decorator

    return wrapper
