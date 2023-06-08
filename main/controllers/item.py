from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from main import app
from main.commons.exceptions import BadRequest, Forbidden, NotFound
from main.db import session
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas import ItemLoadSchema, ItemsLoadSchema, ItemDumpSchema, ItemsDumpSchema

from .helper import get_ownership_item, get_ownership_list_item, load_json, validate_id


@app.get("/items")
@jwt_required(optional=True)
def get_items():
    """
    Get all items of a category
    (Optional) Client can provide a JWT access token to determine ownership
    """
    identity = get_jwt_identity()
    request_data = load_json(ItemsLoadSchema(), None, request_data=request.args)

    query = session.query(ItemModel)

    if "category_id" in request_data:
        # assert if category_id exists
        category = session.get(CategoryModel, request_data["category_id"])
        if not category:
            raise NotFound(error_data={"category_id": ["Not found."]})
        query = query.filter_by(category_id=request_data["category_id"])

    items = (
        query.limit(request_data["items_per_page"])
        .offset(request_data["items_per_page"] * (request_data["page"] - 1))
        .all()
    )
    total_items_count = session.query(ItemModel).count()

    return (
        ItemsDumpSchema().dump(
            {
                "items": get_ownership_list_item(items, identity),
                "items_per_page": request_data["items_per_page"],
                "page": request_data["page"],
                "total_items": total_items_count,
            }
        ),
        200,
    )


@app.get("/items/<string:item_id>")
@jwt_required(optional=True)
def get_item(item_id):
    """
    Get information of an item
    (Optional) Client can provide a JWT access token to determine ownership
    """
    identity = get_jwt_identity()
    item_id = validate_id(item_id, "item_id")

    item = session.get(ItemModel, item_id)

    if not item:
        # item_id not found
        raise NotFound(error_data={"item_id": ["Not found."]})

    return ItemDumpSchema().dump(get_ownership_item(item, identity))


@app.post("/items")
@jwt_required()
def create_item():
    """
    Create an item with an associated category_id
    """
    item_data = load_json(ItemLoadSchema(), request)

    category = session.get(CategoryModel, item_data["category_id"])
    if not category:
        # category_id not found
        raise NotFound(error_data={"category_id": ["Not found."]})

    item_with_similar_name = (
        session.query(ItemModel).filter_by(name=item_data["name"]).first()
    )
    if item_with_similar_name:
        raise BadRequest(error_data={"name": ["Name already belong to another item."]})

    identity = get_jwt_identity()
    item = ItemModel(**item_data, creator_id=identity)

    session.add(item)
    session.commit()

    session.refresh(item)
    return ItemDumpSchema().dump(get_ownership_item(item, identity))


@app.put("/items/<string:item_id>")
@jwt_required()
def update_item(item_id):
    """
    Update an item
    Must be creator
    """
    identity = get_jwt_identity()
    item_data = load_json(ItemLoadSchema(), request)
    item_id = validate_id(item_id, "item_id")

    category = session.get(CategoryModel, item_data["category_id"])
    if not category:
        # category_id not found
        raise NotFound(error_data={"category_id": ["Not found."]})

    item = session.get(ItemModel, item_id)
    if not item:
        # item_id not found, then create new item
        raise NotFound(error_data={"item_id": ["Not found."]})

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

    session.add(item)
    session.commit()

    session.refresh(item)
    return ItemDumpSchema().dump(get_ownership_item(item, identity))


@app.delete("/items/<string:item_id>")
@jwt_required()
def delete_item(item_id):
    """
    Delete an item
    Must be the creator
    """
    identity = get_jwt_identity()
    item_id = validate_id(item_id, "item_id")

    item = session.get(ItemModel, item_id)

    if not item:
        # item_id not found
        raise NotFound(error_data={"item_id": ["Not found."]})

    if identity != item.creator_id:
        # action forbidden (not the creator)
        raise Forbidden()

    session.delete(item)
    session.commit()

    return {}
