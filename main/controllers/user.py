import bcrypt
from flask import request
from flask_jwt_extended import create_access_token

from main import app
from main.commons.exceptions import BadRequest
from main.db import session
from main.models.user import UserModel
from main.schemas import TokenDumpSchema, UserLoadSchema

from .helper import load_json


@app.post("/users")
def create_user():
    """
    Create a new user with unique email address
    """
    user_data = load_json(UserLoadSchema(), request)

    hash_password = bcrypt.hashpw(
        bytes(user_data["password"], "utf-8"), bcrypt.gensalt()
    )
    user = UserModel(email=user_data["email"], password=hash_password)

    # if account with the email has already exist
    existing_user = session.query(UserModel).filter_by(email=user_data["email"]).first()
    if existing_user:
        raise BadRequest(error_message="Email already belong to another account.")

    session.add(user)
    session.commit()

    access_token = create_access_token(identity=user.id)
    return TokenDumpSchema().dump({"access_token": access_token})
