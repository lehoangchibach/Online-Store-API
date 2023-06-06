from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest as BadRequest_no_body

from main import app
from main.commons.exceptions import BadRequest, Forbidden, NotFound
from main.db import session
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas import CategoriesSchema, CategorySchema

from .helper import get_ownership, get_ownership_list


@app.get("/categories")
def get_categories():
    '''
    Get all categories
    (Optional): client can provide a JWT token to determine if they are user of a category or not
    '''
    identity = None
    if request.headers.get("Authorization"):
        verify_jwt_in_request()
        identity = get_jwt_identity()

    try:
        request_data = CategoriesSchema().load(
            {
                "page": request.args.get("page_number") or 0,
                "items_per_page": request.args.get("page_size") or 20,
            }
        )
    except ValidationError as e:
        # validate query parameter
        response = BadRequest()
        response.error_data = e.messages
        return response.to_response()

    q = (
        session.query(CategoryModel)
        .limit(request_data["items_per_page"])
        .offset(request_data["items_per_page"] * request_data["page"])
    )

    categories = q.all()

    return (
        CategoriesSchema().dump(
            {
                "categories": get_ownership_list(categories, identity),
                "items_per_page": request_data["items_per_page"],
                "page": request_data["page"],
                "total_items": len(categories),
            }
        ),
        200,
    )


@app.post("/categories")
@jwt_required()
def create_category():
    '''
    Create a category
    '''
    try:
        category_data = CategorySchema().load(request.json)
    except ValidationError as e:
        # validate request data
        response = BadRequest()
        response.error_data = e.messages
        return response.to_response()
    except BadRequest_no_body:
        # request with no body
        response = BadRequest()
        response.error_data = {"name": "DNE"}
        return response.to_response()

    identity = get_jwt_identity()
    category = CategoryModel(**category_data, creator_id=identity)

    try:
        session.add(category)
        session.commit()
    except IntegrityError:
        # category name has already exist
        response = BadRequest()
        response.error_data = {"name": "Name already belong to another category"}
        return response.to_response()

    session.refresh(category)
    return CategorySchema().dump(get_ownership(category, identity)), 200


@app.delete("/categories/<string:category_id>")
@jwt_required()
def delete_category(category_id):
    '''
    Delete a category
    Must be the creator
    '''
    try:
        category_id = int(category_id)
    except ValueError:
        # validate category_id
        response = BadRequest()
        response.error_data = {"category_id": "Not an int"}
        return response.to_response()

    category = session.get(CategoryModel, category_id)
    if not category:
        # category_id not exist
        response = NotFound()
        response.error_data = {"category_id": "Not found"}
        return response.to_response()

    identity = get_jwt_identity()
    if identity != category.creator_id:
        # client is not the creator
        response = Forbidden()
        return response.to_response()

    q = session.query(ItemModel).filter_by(category_id=category.id)
    items = q.all()


    for item in items:
        session.delete(item)
    session.commit()

    session.delete(category)
    session.commit()

    return "", 200
