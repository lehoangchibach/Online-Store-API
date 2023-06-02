from flask import request
from marshmallow import ValidationError
from main.schemas import ItemSchema, ItemsSchema
from main.db import session
from main.models.item import ItemModel
from main.commons.exceptions import BadRequest, NotFound, Forbidden
from .helper import get_ownership, get_ownership_list
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, jwt_required
from werkzeug.exceptions import BadRequest as BadRequest_no_body
from sqlalchemy.exc import IntegrityError

from main import app


@app.get("/items")
def get_items():
    identity = None
    if request.headers.get("Authorization"):
        verify_jwt_in_request()
        identity = get_jwt_identity()

    try:
        request_data = ItemsSchema().load({
            "page": request.args.get("page_number") or 0,
            "items_per_page": request.args.get("page_size") or 20,
            "category_id": request.args.get("category_id")
        })
    except ValidationError as e:
        response = BadRequest()
        response.error_data = e.messages
        return response.to_response()

    q = session.query(ItemModel).filter_by(category_id=request_data["category_id"]) \
        .limit(request_data["items_per_page"]) \
        .offset(request_data["items_per_page"] * request_data["page"])

    items = q.all()

    return ItemsSchema().dump({
        "items": get_ownership_list(items, identity),
        "items_per_page": request_data["items_per_page"],
        "page": request_data["page"],
        "total_items": len(items)
    }), 200


@app.get("/items/<string:item_id>")
def get_item(item_id):
    identity = None
    if request.headers.get("Authorization"):
        authorization = verify_jwt_in_request()
        identity = get_jwt_identity()

    try:
        int(item_id)
    except ValueError:
        response = BadRequest()
        response.error_data = {"item_id": "Not an int"}
        return response.to_response()

    item_id = int(item_id)

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
        response.error_data = {"name": "DNE",
                               "description": "DNE",
                               "category_id": "DNE"}
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

    return ItemSchema().dump({
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "is_creator": identity == item.creator_id,
        "category_id": item.category_id
    }), 200


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
        response.error_data = {"name": "DNE",
                               "description": "DNE",
                               "category_id": "DNE"}
        return response.to_response()

    try:
        int(item_id)
    except ValueError:
        response = BadRequest()
        response.error_data = {"item_id": "Not an int"}
        return response.to_response()

    identity = get_jwt_identity()

    item_id = int(item_id)
    item = session.query(ItemModel).get(item_id)

    if not item:
        response = NotFound()
        response.error_data = {"item_id": "Not found"}
        return response.to_response()

    if identity != item.id:
        response = Forbidden()
        return response.to_response()

    try:
        session.add(item)
        session.commit()
    except IntegrityError:
        response = BadRequest()
        response.error_data = {"name": "Name already belong to another item"}
        return response.to_response()

    return ItemSchema().dump(get_ownership(item, identity)), 200
