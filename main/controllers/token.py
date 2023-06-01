from flask import request
from marshmallow import ValidationError
from ..schemas import UserSchema, TokenSchema, ErrorSchema
from flask_jwt_extended import create_access_token
from ..db import session
from ..models.user import UserModel
import bcrypt

from main import app


@app.post("/tokens")
def login():
    try:
        user_data = UserSchema().load(request.json)
    except ValidationError as e:
        return ErrorSchema().dump({
            "error_code": 400000,
            "error_data": e.messages,
            "error_message": "Bad Request"
        }), 400

    q = session.query(UserModel).filter_by(email=user_data["email"])
    user = q.one_or_none()
    if not user:
        return

    is_valid_user = bcrypt.checkpw(bytes(user_data["password"], "ascii"),
                                   bytes(user.password, "ascii"))

    if not is_valid_user:
        return

    access_token = create_access_token(identity=1)
    return TokenSchema().dump({"access_token": access_token}), 200
