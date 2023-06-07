from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from main import app
from main.commons.exceptions import BadRequest, Forbidden, NotFound
from main.db import session
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas import CategoriesSchema, CategorySchema

from .helper import get_ownership, get_ownership_list, load_json, validate_id


@app.get("/categories")
@jwt_required(optional=True)
def get_categories():
    """
    Get all categories
    (Optional): client can provide a JWT token to determine
        if they are user of a category or not
    """
    identity = get_jwt_identity()

    request_data = load_json(CategoriesSchema(), None, request_data=request.args)

    categories = (
        session.query(CategoryModel)
        .limit(request_data["items_per_page"])
        .offset(request_data["items_per_page"] * (request_data["page"] - 1))
        .all()
    )
    total_categories_count = session.query(CategoryModel).count()

    return CategoriesSchema().dump(
        {
            "categories": get_ownership_list(categories, identity),
            "items_per_page": request_data["items_per_page"],
            "page": request_data["page"],
            "total_items": total_categories_count,
        }
    )


@app.post("/categories")
@jwt_required()
def create_category():
    """
    Create a category
    """
    identity = get_jwt_identity()

    category_data = load_json(CategorySchema(), request)

    category = CategoryModel(**category_data, creator_id=identity)
    category_with_same_name = (
        session.query(CategoryModel).filter_by(name=category_data["name"]).first()
    )

    if category_with_same_name:
        raise BadRequest(
            error_data={"name": ["Name already belong to another category."]}
        )

    session.add(category)
    session.commit()

    session.refresh(category)
    return CategorySchema().dump(get_ownership(category, identity))


@app.delete("/categories/<string:category_id>")
@jwt_required()
def delete_category(category_id):
    """
    Delete a category
    Must be the creator
    """
    identity = get_jwt_identity()

    category_id = validate_id(category_id)

    category = session.get(CategoryModel, category_id)
    if not category:
        # category_id not exist
        raise NotFound(error_data={"category_id": ["Not found."]})

    if identity != category.creator_id:
        # client is not the creator
        raise Forbidden()

    items = session.query(ItemModel).filter_by(category_id=category.id).all()

    for item in items:
        session.delete(item)
    session.commit()

    session.delete(category)
    session.commit()

    return {}
