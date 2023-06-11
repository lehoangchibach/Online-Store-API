from flask import request
from flask_jwt_extended import jwt_required

from main import app
from main.commons.exceptions import BadRequest, Forbidden, NotFound
from main.db import session
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas import (
    ItemDumpSchema,
    ItemLoadSchema,
    ItemsDumpSchema,
    ItemsLoadSchema,
)

from ..commons.decorators import get_by_id, get_identity
from .helper import load_json


@app.get("/items")
@jwt_required(optional=True)
@get_identity
def get_items(identity):
    """
    Get all items of a category
    (Optional) Client can provide a JWT access token to determine ownership
    """
    request_data = load_json(ItemsLoadSchema(), request)

    query = session.query(ItemModel)

    if "category_id" in request_data:
        # assert if category_id exists
        category = session.get(CategoryModel, request_data["category_id"])
        if not category:
            raise NotFound(error_message="Category_id not found.")
        query = query.filter_by(category_id=request_data["category_id"])

    items = (
        query.limit(request_data["items_per_page"])
        .offset(request_data["items_per_page"] * (request_data["page"] - 1))
        .all()
    )
    total_items_count = session.query(ItemModel).count()

    for item in items:
        item.is_creator = identity == item.creator_id
    return ItemsDumpSchema().dump(
        {
            "items": items,
            "items_per_page": request_data["items_per_page"],
            "page": request_data["page"],
            "total_items": total_items_count,
        }
    )


@app.get("/items/<int:item_id>")
@jwt_required(optional=True)
@get_by_id(ItemModel, "item_id")
@get_identity
def get_item(identity, item, item_id):
    """
    Get information of an item
    (Optional) Client can provide a JWT access token to determine ownership
    """

    item.is_creator = identity == item.creator_id
    return ItemDumpSchema().dump(item)


@app.post("/items")
@jwt_required()
@get_identity
def create_item(identity):
    """
    Create an item with an associated category_id
    """
    item_data = load_json(ItemLoadSchema(), request)

    category = session.get(CategoryModel, item_data["category_id"])
    if not category:
        # category_id not found
        raise BadRequest(error_message="Category_id not found.")

    existing_item = session.query(ItemModel).filter_by(name=item_data["name"]).first()
    if existing_item:
        raise BadRequest(error_data={"name": ["Name already belong to another item."]})

    item = ItemModel(**item_data, creator_id=identity)

    session.add(item)
    session.commit()

    item.is_creator = identity == item.creator_id
    return ItemDumpSchema().dump(item)


@app.put("/items/<int:item_id>")
@jwt_required()
@get_by_id(ItemModel, "item_id")
@get_identity
def update_item(identity, item, item_id):
    """
    Update an item
    Must be creator
    """
    item_data = load_json(ItemLoadSchema(), request)

    category = session.get(CategoryModel, item_data["category_id"])
    if not category:
        # category_id not found
        raise BadRequest(error_message="Category_id not found.")

    if identity != item.creator_id:
        # action forbidden (not creator)
        raise Forbidden()

    item_with_same_name = (
        session.query(ItemModel).filter_by(name=item_data["name"]).first()
    )
    if item_with_same_name and item_with_same_name.id != item.id:
        raise BadRequest(error_data={"name": ["Item's name has already exists."]})

    for key, value in item_data.items():
        setattr(item, key, value)

    session.commit()

    item.is_creator = identity == item.creator_id
    return ItemDumpSchema().dump(item)


@app.delete("/items/<int:item_id>")
@jwt_required()
@get_by_id(ItemModel, "item_id")
@get_identity
def delete_item(identity, item, item_id):
    """
    Delete an item
    Must be the creator
    """
    if identity != item.creator_id:
        # action forbidden (not the creator)
        raise Forbidden()

    session.delete(item)
    session.commit()

    return {}
