from importlib import import_module

from flask import Flask
from flask_cors import CORS

from . import db
from ._config import config
from .commons.error_handlers import register_error_handlers

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .schemas.exceptions import ErrorSchema
from .commons.exceptions import Unauthorized

app = Flask(__name__)
app.config.from_object(config)

CORS(app)


def register_subpackages() -> None:
    from main import models

    for m in models.__all__:
        import_module("main.models." + m)

    import main.controllers


register_subpackages()
register_error_handlers(app)


# https://flask.palletsprojects.com/en/2.2.x/patterns/sqlalchemy/#declarative
# To use SQLAlchemy in a declarative way with your application,
# you just have to put the following code into your application module.
# Flask will automatically remove database sessions at the end of the request
# or when the application shuts down:
@app.teardown_appcontext
def shutdown_session(*_, **__):  # type: ignore
    db.session.remove()


jwt = JWTManager(app)
migrate = Migrate(app, SQLAlchemy(app))


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    response = Unauthorized()
    response.error_data = {"access_token": "Expired access token"}
    return response.to_response()


@jwt.unauthorized_loader
def unauthorized_loader_callback(message):
    response = Unauthorized()
    response.error_data = {"access_token": message}
    return response.to_response()
