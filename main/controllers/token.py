from flask import request
from marshmallow import ValidationError
from main.schemas import UserSchema, TokenSchema
from flask_jwt_extended import create_access_token
from main.db import session
from main.models.user import UserModel
from main.commons.exceptions import BadRequest, Unauthorized, NotFound
import bcrypt


from main import app


@app.post("/tokens")
def login():
    try:
        user_data = UserSchema().load(request.json)
    except ValidationError as e:
        response = BadRequest()
        response.error_data = e.messages
        return response.to_response()

    q = session.query(UserModel).filter_by(email=user_data["email"])
    user = q.first()
    if not user:
        response = NotFound()
        response.error_data = {"email": "Not found"}
        return response.to_response()

    is_valid_user = bcrypt.checkpw(bytes(user_data["password"], "ascii"),
                                   bytes(user.password, "ascii"))

    if not is_valid_user:
        response = Unauthorized()
        response.error_data = {"password": "Password is not correct"}
        return response.to_response()

    access_token = create_access_token(identity=user.id)
    return TokenSchema().dump({"access_token": access_token}), 200
