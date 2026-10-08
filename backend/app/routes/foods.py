from flask import Blueprint, request
from app.services.food_service import get_foods, get_food_by_id, create_food, update_food, delete_food
from app.utils.helpers import success_response, error_response
from app.utils.decorators import role_required

foods_bp = Blueprint('foods', __name__, url_prefix='/api/foods')

@foods_bp.route('/', methods=['GET'])
def list_foods():
    filters = {
        'restaurant_id': request.args.get('restaurant_id'),
        'category_id': request.args.get('category_id'),
        'search': request.args.get('search'),
        'is_veg': request.args.get('is_veg'),
        'is_available': request.args.get('is_available', 'true').lower() == 'true'
    }

    try:
        foods = get_foods(filters)
        return success_response([f.to_dict() for f in foods], "Foods retrieved")
    except Exception as e:
        return error_response(str(e), 500)

@foods_bp.route('/<int:id>', methods=['GET'])
def get_food(id):
    try:
        food = get_food_by_id(id)
        if food:
            return success_response(food.to_dict(), "Food retrieved")
        return error_response("Food not found", 404)
    except Exception as e:
        return error_response(str(e), 500)

@foods_bp.route('/', methods=['POST'])
@role_required('restaurant', 'admin')
def add_food():
    data = request.get_json()
    try:
        food = create_food(data)
        return success_response(food.to_dict(), "Food created", 201)
    except Exception as e:
        return error_response(str(e), 500)

@foods_bp.route('/<int:id>', methods=['PUT'])
@role_required('restaurant', 'admin')
def edit_food(id):
    data = request.get_json()
    try:
        food = update_food(id, data)
        if food:
            return success_response(food.to_dict(), "Food updated")
        return error_response("Food not found", 404)
    except Exception as e:
        return error_response(str(e), 500)

@foods_bp.route('/<int:id>', methods=['DELETE'])
@role_required('restaurant', 'admin')
def remove_food(id):
    try:
        success = delete_food(id)
        if success:
            return success_response(None, "Food deleted")
        return error_response("Food not found", 404)
    except Exception as e:
        return error_response(str(e), 500)
