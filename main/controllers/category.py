from typing import Any

from flask_jwt_extended import jwt_required

from main import app
from main.commons.exceptions import BadRequest, Forbidden
from main.db import session
from main.models.category import CategoryModel
from main.schemas import (
    CategoriesSchema,
    CategoryCreateSchema,
    CategorySchema,
    PaginationSchema,
)

from ..commons.decorators import get_by_id, get_identity, load_json


@app.get("/categories")
@jwt_required(optional=True)
@get_identity
@load_json(PaginationSchema())
def get_categories(request_data: dict[str, Any], identity: int | None):
    """
    Get all categories
    (Optional): client can provide a JWT token to determine
        if they are user of a category or not
    """
    categories = (
        session.query(CategoryModel)
        .limit(request_data["items_per_page"])
        .offset(request_data["items_per_page"] * (request_data["page"] - 1))
        .all()
    )
    total_categories_count = session.query(CategoryModel).count()

    for category in categories:
        category.is_creator = identity == category.creator_id
    return CategoriesSchema().dump(
        {
            "categories": categories,
            "items_per_page": request_data["items_per_page"],
            "page": request_data["page"],
            "total_items": total_categories_count,
        }
    )


@app.post("/categories")
@jwt_required()
@get_identity
@load_json(CategoryCreateSchema())
def create_category(request_data: dict[str, Any], identity: int):
    """
    Create a category
    """
    category = CategoryModel(**request_data, creator_id=identity)
    existing_category = (
        session.query(CategoryModel).filter_by(name=request_data["name"]).first()
    )

    if existing_category:
        raise BadRequest(
            error_data={"name": ["Name already belong to another category."]}
        )

    session.add(category)
    session.commit()

    category.is_creator = category.creator_id == identity
    return CategorySchema().dump(category)


@app.delete("/categories/<int:category_id>")
@jwt_required()
@get_by_id(CategoryModel, "category_id")
@get_identity
def delete_category(identity: int, item: type[CategoryModel], **__):
    """
    Delete a category
    Must be the creator
    """

    if identity != item.creator_id:
        # client is not the creator
        raise Forbidden()

    session.delete(item)
    session.commit()

    return {}
