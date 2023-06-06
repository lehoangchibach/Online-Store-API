import os
import sys
from importlib import import_module
from pathlib import Path

import pytest
from alembic.command import upgrade
from alembic.config import Config
from sqlalchemy import text, create_engine
from sqlalchemy.orm import scoped_session

from main import app as _app
from main import db
from main import migrate
from main.libs.log import ServiceLogger

from main.models.user import UserModel
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.base import BaseModel
from sqlalchemy.schema import MetaData

logger = ServiceLogger(__name__)

if os.getenv("ENVIRONMENT") != "test":
    logger.error(message='Tests should be run with "ENVIRONMENT=test"')
    sys.exit(1)

ALEMBIC_CONFIG = (Path(__file__).parents[1] / "alembic.ini").resolve().as_posix()


@pytest.fixture(scope="session", autouse=True)
def app():
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="session", autouse=True)
def create_database(app):
    alembic_config = Config(ALEMBIC_CONFIG)
    # upgrade(alembic_config, "heads")

    from main._config import config
    engine = create_engine(
        url=config.SQLALCHEMY_DATABASE_URI,
        **config.SQLALCHEMY_ENGINE_OPTIONS,
    )
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def session():
    from sqlalchemy.orm import sessionmaker

    connection = db.session.bind.engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    db.session = scoped_session(session_factory)

    yield

    transaction.rollback()
    connection.close()
    db.session.close()


@pytest.fixture(scope="function", autouse=True)
def client(app):
    return app.test_client()
