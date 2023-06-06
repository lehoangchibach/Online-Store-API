from flask import request
from marshmallow import ValidationError
from main.schemas import TokenSchema, UserSchema
from main.models.user import UserModel
from main.db import session
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest as BadRequest_no_body
from main.commons.exceptions import BadRequest
import bcrypt

from main import app


@app.post("/users")
def create_user():
    '''
    Create a new user with unique email address
    '''
    try:
        user_data = UserSchema().load(request.json)
    except ValidationError as e:
        # validate email address and password
        response = BadRequest()
        response.error_data = e.messages
        return response.to_response()
    except BadRequest_no_body:
        # request with no body
        response = BadRequest()
        response.error_data = {"email": "DNE",
                               "password": "DNE"}
        return response.to_response()

    hash_password = bcrypt.hashpw(bytes(user_data["password"], "ascii"), bcrypt.gensalt())
    user = UserModel(
        email=user_data["email"],
        password=hash_password
    )

    try:
        session.add(user)
        session.commit()
    except IntegrityError:
        # email address has already existed
        response = BadRequest()
        response.error_data = {"email": "Email already belong to another account."}
        return response.to_response()


    # session.refresh(user)
    access_token = create_access_token(identity=user.id)

    return TokenSchema().dump({"access_token": access_token}), 200
