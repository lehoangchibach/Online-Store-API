from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest as BadRequest_no_body

from main import app
from main.commons.exceptions import BadRequest, Forbidden, NotFound
from main.db import session
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas import ItemSchema, ItemsSchema

from .helper import get_ownership, get_ownership_list


@app.get("/items")
def get_items():
    identity = None
    if request.headers.get("Authorization"):
        verify_jwt_in_request()
        identity = get_jwt_identity()

    try:
        request_data = ItemsSchema().load(
            {
                "page": request.args.get("page_number") or 0,
                "items_per_page": request.args.get("page_size") or 20,
                "category_id": request.args.get("category_id"),
            }
        )
    except ValidationError as e:
        response = BadRequest()
        response.error_data = e.messages
        return response.to_response()

    q = (
        session.query(ItemModel)
        .filter_by(category_id=request_data["category_id"])
        .limit(request_data["items_per_page"])
        .offset(request_data["items_per_page"] * request_data["page"])
    )

    items = q.all()

    return (
        ItemsSchema().dump(
            {
                "items": get_ownership_list(items, identity),
                "items_per_page": request_data["items_per_page"],
                "page": request_data["page"],
                "total_items": len(items),
            }
        ),
        200,
    )


@app.get("/items/<string:item_id>")
def get_item(item_id):
    identity = None
    if request.headers.get("Authorization"):
        verify_jwt_in_request()
        identity = get_jwt_identity()

    try:
        item_id = int(item_id)
    except ValueError:
        response = BadRequest()
        response.error_data = {"item_id": "Not an int"}
        return response.to_response()

    item = session.query(ItemModel).get(item_id)

    if not item:
        response = NotFound()
        response.error_data = {"item_id": "Not found"}
        return response.to_response()

    return ItemSchema().dump(get_ownership(item, identity)), 200


@app.post("/items")
@jwt_required()
def create_item():
    try:
        item_data = ItemSchema().load(request.json)
    except ValidationError as e:
        response = BadRequest()
        response.error_data = e.messages
        return response.to_response()
    except BadRequest_no_body:
        response = BadRequest()
        response.error_data = {
            "name": "DNE",
            "description": "DNE",
            "category_id": "DNE",
        }
        return response.to_response()

    identity = get_jwt_identity()
    item = ItemModel(**item_data, creator_id=identity)

    try:
        session.add(item)
        session.commit()
    except IntegrityError:
        response = BadRequest()
        response.error_data = {"name": "Name already belong to another item"}
        return response.to_response()

    session.refresh(item)
    return ItemSchema().dump(get_ownership(item, identity)), 200


@app.put("/items/<string:item_id>")
@jwt_required()
def update_item(item_id):
    try:
        item_data = ItemSchema().load(request.json)
    except ValidationError as e:
        response = BadRequest()
        response.error_data = e.messages
        return response.to_response()
    except BadRequest_no_body:
        response = BadRequest()
        response.error_data = {
            "name": "DNE",
            "description": "DNE",
            "category_id": "DNE",
        }
        return response.to_response()

    try:
        item_id = int(item_id)
    except ValueError:
        response = BadRequest()
        response.error_data = {"item_id": "Not an int"}
        return response.to_response()

    category = session.query(CategoryModel).get(item_data["category_id"])

    if not category:
        response = NotFound()
        response.error_data = {"category_id": "Not found"}
        return response.to_response()

    identity = get_jwt_identity()
    item = session.query(ItemModel).get(item_id)

    if not item:
        item = ItemModel(**item_data, id=item_id, creator_id=identity)

    if identity != item.creator_id:
        response = Forbidden()
        return response.to_response()

    for key, value in item_data.items():
        setattr(item, key, value)

    try:
        session.add(item)
        session.commit()
    except IntegrityError:
        response = BadRequest()
        response.error_data = {"name": "Name already belong to another item"}
        return response.to_response()

    session.refresh(item)
    return ItemSchema().dump(get_ownership(item, identity)), 200


@app.delete("/items/<string:item_id>")
@jwt_required()
def delete_item(item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        response = BadRequest()
        response.error_data = {"item_id": "Not an int"}
        return response.to_response()

    item = session.query(ItemModel).get(item_id)

    if not item:
        response = NotFound()
        response.error_data = {"item_id": "Not found"}
        return response.to_response()

    identity = get_jwt_identity()
    if identity != item.creator_id:
        response = Forbidden()
        return response.to_response()

    session.delete(item)
    session.commit()

    return "", 200
