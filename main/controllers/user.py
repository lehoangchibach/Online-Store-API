from flask import request
from marshmallow import ValidationError
from ..schemas import TokenSchema, UserSchema, ErrorSchema
from ..models.user import UserModel
from ..db import session
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
import bcrypt

from main import app


@app.post("/users")
def create_user():
    try:
        user_data = UserSchema().load(request.json)
    except ValidationError as e:
        return ErrorSchema().dump({
            "error_code": 400000,
            "error_data": e.messages,
            "error_message": "Bad Request"
        }), 400

    hash_password = bcrypt.hashpw(bytes(user_data["password"], "ascii"), bcrypt.gensalt())
    user = UserModel(
        email=user_data["email"],
        password=hash_password
    )

    try:
        session.add(user)
        session.commit()
    except IntegrityError as e:
        return ErrorSchema().dump({
            "error_code": 400000,
            "error_data": {"email": "Email already belong to another account."},
            "error_message": "Bad Request"
        }), 400

    access_token = create_access_token(identity=1)

    return TokenSchema().dump({"access_token": access_token}), 200
