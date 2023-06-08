import bcrypt
from flask import request
from flask_jwt_extended import create_access_token

from main import app
from main.commons.exceptions import NotFound, Unauthorized
from main.db import session
from main.models.user import UserModel
from main.schemas import TokenDumpSchema, UserLoadSchema

from .helper import load_json


@app.post("/tokens")
def login():
    """
    Login user and return a JWT access token
    """
    user_data = load_json(UserLoadSchema(), request)

    user = session.query(UserModel).filter_by(email=user_data["email"]).first()
    if not user:
        # request's credential does not exist
        raise NotFound(error_data={}, error_message="Email or password is not correct.")

    is_password_correct = bcrypt.checkpw(
        bytes(user_data["password"], "utf-8"), bytes(user.password, "utf-8")
    )

    if not is_password_correct:
        # password is not correct
        raise Unauthorized(
            error_data={}, error_message="Email or password is not correct."
        )

    access_token = create_access_token(identity=user.id)
    return TokenDumpSchema().dump({"access_token": access_token})
