import bcrypt
from flask_jwt_extended import create_access_token

from main import app
from main.commons.exceptions import BadRequest
from main.db import session
from main.models.user import UserModel
from main.schemas import TokenSchema

from ..commons.decorators import load_json
from ..schemas.token import TokenLoginSchema


@app.post("/tokens")
@load_json(TokenLoginSchema())
def login(request_data):
    """
    Login user and return a JWT access token
    """
    user = session.query(UserModel).filter_by(email=request_data["email"]).first()
    if not user:
        # request's credential does not exist
        raise BadRequest(error_message="Email or password is not correct.")

    is_password_correct = bcrypt.checkpw(
        bytes(request_data["password"], "utf-8"), bytes(user.password, "utf-8")
    )

    if not is_password_correct:
        # password is not correct
        raise BadRequest(error_message="Email or password is not correct.")

    access_token = create_access_token(identity=user.id)
    return TokenSchema().dump({"access_token": access_token})
