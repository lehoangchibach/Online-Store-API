from importlib import import_module

from flask import Flask
from flask_cors import CORS

from . import db
from ._config import config
from .commons.error_handlers import register_error_handlers

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
