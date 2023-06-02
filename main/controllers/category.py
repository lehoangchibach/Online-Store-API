from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, jwt_required
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest as BadRequest_no_body

from main import app
from .helper import get_ownership_list
from main.commons.exceptions import BadRequest, NotFound, Forbidden
from main.db import session
from main.models.category import CategoryModel
from main.schemas import CategorySchema, CategoriesSchema


@app.get("/categories")
def get_categories():
    identity = None
    if request.headers.get("Authorization"):
        verify_jwt_in_request()
        identity = get_jwt_identity()

    try:
        request_data = CategoriesSchema().load({
            "page": request.args.get("page_number") or 0,
            "items_per_page": request.args.get("page_size") or 20
        })
    except ValidationError as e:
        response = BadRequest()
        response.error_data = e.messages
        return response.to_response()

    q = session.query(CategoryModel).limit(request_data["items_per_page"]) \
        .offset(request_data["items_per_page"] * request_data["page"])

    categories = q.all()

    return CategoriesSchema().dump({
        "categories": get_ownership_list(categories, identity),
        "items_per_page": request_data["items_per_page"],
        "page": request_data["page"],
        "total_items": len(categories)
    }), 200


@app.post("/categories")
@jwt_required()
def create_category():
    try:
        category_data = CategorySchema().load(request.json)
    except ValidationError as e:
        response = BadRequest()
        response.error_data = e.messages
        return response.to_response()
    except BadRequest_no_body:
        response = BadRequest()
        response.error_data = {"name": "DNE"}
        return response.to_response()

    identity = get_jwt_identity()
    category = CategoryModel(**category_data,
                             creator_id=identity)

    try:
        session.add(category)
        session.commit()
    except IntegrityError:
        response = BadRequest()
        response.error_data = {"name": "Name already belong to another category"}
        return response.to_response()

    return CategorySchema().dump({
        "id": category.id,
        "name": category.name,
        "is_creator": identity == category.creator_id
    }), 200


@app.delete("/categories/<string:category_id>")
@jwt_required()
def delete_category(category_id):
    try:
        int(category_id)
    except ValueError:
        response = BadRequest()
        response.error_data = {"item_id": "Not an int"}
        return response.to_response()

    category_id = int(category_id)

    category = session.query(CategoryModel).get(category_id)
    if not category:
        response = NotFound()
        response.error_data = {"category_id": "Not found"}
        return response.to_response()

    identity = get_jwt_identity()
    if identity != category.creator_id:
        response = Forbidden()
        return response.to_response()

    session.delete(category)
    session.commit()

    return '', 200
