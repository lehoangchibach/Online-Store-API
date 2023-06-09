from functools import wraps

from flask import request
from flask_jwt_extended import get_jwt_identity

from main.commons.exceptions import NotFound
from main.db import session


def get_by_id(model, path_variable):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            item_id = request.view_args[path_variable]
            item = session.get(model, item_id)
            if not item:
                raise NotFound(error_message=f"{path_variable.capitalize()} not found.")
            return func(item, *args, **kwargs)

        return decorator

    return wrapper


def get_identity(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        identity = get_jwt_identity()
        return func(identity, *args, **kwargs)

    return decorator
