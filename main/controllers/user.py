import bcrypt
from flask_jwt_extended import create_access_token

from main import app
from main.commons.decorators import load_json
from main.commons.exceptions import BadRequest
from main.db import session
from main.models.user import UserModel
from main.schemas import TokenSchema, UserCreateSchema

# from .helper import load_json


@app.post("/users")
@load_json(UserCreateSchema())
def create_user(request_data):
    """
    Create a new user with unique email address
    """

    hash_password = bcrypt.hashpw(
        bytes(request_data["password"], "utf-8"), bcrypt.gensalt()
    )
    user = UserModel(email=request_data["email"], password=hash_password)

    # if account with the email has already exist
    existing_user = (
        session.query(UserModel).filter_by(email=request_data["email"]).first()
    )
    if existing_user:
        raise BadRequest(error_message="Email already belong to another account.")

    session.add(user)
    session.commit()

    access_token = create_access_token(identity=user.id)
    return TokenSchema().dump({"access_token": access_token})
