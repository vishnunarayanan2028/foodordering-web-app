from flask import Blueprint, request
from app.services.food_service import get_categories, get_category_by_id, create_category, update_category, delete_category
from app.utils.helpers import success_response, error_response
from app.utils.decorators import role_required

categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@categories_bp.route('/', methods=['GET'])
def list_categories():
    try:
        categories = get_categories()
        data = []
        for c in categories:
            d = c.to_dict()
            d['food_count'] = len(c.foods)
            data.append(d)
        return success_response(data, "Categories retrieved")
    except Exception as e:
        return error_response(str(e), 500)

@categories_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    try:
        category = get_category_by_id(id)
        if category:
            data = category.to_dict()
            data['foods'] = [f.to_dict() for f in category.foods]
            return success_response(data, "Category retrieved")
        return error_response("Category not found", 404)
    except Exception as e:
        return error_response(str(e), 500)

@categories_bp.route('/', methods=['POST'])
@role_required('restaurant', 'admin')
def add_category():
    data = request.get_json()
    try:
        category = create_category(data)
        return success_response(category.to_dict(), "Category created", 201)
    except Exception as e:
        return error_response(str(e), 500)

@categories_bp.route('/<int:id>', methods=['PUT'])
@role_required('restaurant', 'admin')
def edit_category(id):
    data = request.get_json()
    try:
        category = update_category(id, data)
        if category:
            return success_response(category.to_dict(), "Category updated")
        return error_response("Category not found", 404)
    except Exception as e:
        return error_response(str(e), 500)

@categories_bp.route('/<int:id>', methods=['DELETE'])
@role_required('restaurant', 'admin')
def remove_category(id):
    try:
        success = delete_category(id)
        if success:
            return success_response(None, "Category deleted")
        return error_response("Category not found", 404)
    except Exception as e:
        return error_response(str(e), 500)
