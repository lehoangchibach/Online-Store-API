from flask import request
from flask_jwt_extended import jwt_required

from main import app
from main.commons.exceptions import BadRequest, Forbidden
from main.db import session
from main.models.category import CategoryModel
from main.schemas import (
    CategoriesDumpSchema,
    CategoryDumpSchema,
    CategoryLoadSchema,
    PaginationSchema,
)

from ..commons.decorators import get_by_id, get_identity
from .helper import load_json


@app.get("/categories")
@jwt_required(optional=True)
@get_identity
def get_categories(identity):
    """
    Get all categories
    (Optional): client can provide a JWT token to determine
        if they are user of a category or not
    """
    request_data = load_json(PaginationSchema(), request)

    categories = (
        session.query(CategoryModel)
        .limit(request_data["items_per_page"])
        .offset(request_data["items_per_page"] * (request_data["page"] - 1))
        .all()
    )
    total_categories_count = session.query(CategoryModel).count()

    for category in categories:
        category.is_creator = identity == category.creator_id
    return CategoriesDumpSchema().dump(
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
def create_category(identity):
    """
    Create a category
    """
    category_data = load_json(CategoryLoadSchema(), request)

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

    category.is_creator = category.creator_id == identity
    return CategoryDumpSchema().dump(category)


@app.delete("/categories/<int:category_id>")
@jwt_required()
@get_by_id(CategoryModel, "category_id")
@get_identity
def delete_category(identity, category, category_id):
    """
    Delete a category
    Must be the creator
    """

    if identity != category.creator_id:
        # client is not the creator
        raise Forbidden()

    session.delete(category)
    session.commit()

    return {}
