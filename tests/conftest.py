import datetime
import os
import sys
from pathlib import Path

import bcrypt
import pytest
from alembic.config import Config
from flask_jwt_extended import create_access_token
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session

from main import app as _app
from main import db
from main.libs.log import ServiceLogger
from main.models.base import BaseModel
from main.models.category import CategoryModel
from main.models.user import UserModel

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
    Config(ALEMBIC_CONFIG)
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


@pytest.fixture(scope="session", autouse=True)
def create_fixture_users():
    user_datas = [
        {"email": "testemail@gmail.com", "password": "Password123"},
        {"email": "second_testemail@gmail.com", "password": "Password123"},
    ]

    for user_data in user_datas:
        hash_password = bcrypt.hashpw(
            bytes(user_data["password"], "utf-8"), bcrypt.gensalt()
        )
        user = UserModel(email=user_data["email"], password=hash_password)
        db.session.add(user)

    db.session.commit()


@pytest.fixture(scope="session", autouse=True)
def create_fixture_category(create_fixture_users):
    user = db.session.query(UserModel).filter_by(email="testemail@gmail.com").first()

    category_names = [
        "fixture_category",
        "category_for_delete_successfully",
        "category_for_delete_failed_forbidden",
    ]
    for name in category_names:
        category = CategoryModel(name=name, creator_id=user.id)
        db.session.add(category)

    db.session.commit()


@pytest.fixture
def get_fixture_valid_access_token_user_1():
    user = db.session.query(UserModel).filter_by(email="testemail@gmail.com").first()
    return create_access_token(identity=user.id)


@pytest.fixture
def get_fixture_valid_access_token_user_2():
    user = (
        db.session.query(UserModel)
        .filter_by(email="second_testemail@gmail.com")
        .first()
    )
    return create_access_token(identity=user.id)


@pytest.fixture
def get_fixture_invalid_access_token():
    user = db.session.query(UserModel).filter_by(email="testemail@gmail.com").first()
    return create_access_token(
        identity=user.id, expires_delta=datetime.timedelta(seconds=-1)
    )


@pytest.fixture
def get_fixture_category():
    return db.session.query(CategoryModel).filter_by(name="fixture_category").first()


@pytest.fixture
def get_category_for_delete_successfully(create_fixture_users):
    return (
        db.session.query(CategoryModel)
        .filter_by(name="category_for_delete_successfully")
        .first()
    )


@pytest.fixture
def get_category_for_delete_failed_forbidden(create_fixture_users):
    return (
        db.session.query(CategoryModel)
        .filter_by(name="category_for_delete_failed_forbidden")
        .first()
    )
