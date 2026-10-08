from flask import Blueprint, request, g
from app.services.cart_service import get_cart, add_to_cart, update_cart_item, remove_cart_item, clear_cart
from app.utils.helpers import success_response, error_response
from app.utils.decorators import login_required

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_bp.route('/', methods=['GET'])
@login_required()
def view_cart():
    try:
        cart_data = get_cart(g.current_user.id)
        return success_response(cart_data, "Cart retrieved")
    except Exception as e:
        return error_response(str(e), 500)

@cart_bp.route('/items', methods=['POST'])
@login_required()
def add_item():
    data = request.get_json()
    try:
        add_to_cart(g.current_user.id, data.get('food_id'), data.get('quantity', 1))
        cart_data = get_cart(g.current_user.id)
        return success_response(cart_data, "Item added to cart")
    except Exception as e:
        return error_response(str(e), 500)

@cart_bp.route('/items/<int:id>', methods=['PUT'])
@login_required()
def update_item(id):
    data = request.get_json()
    try:
        update_cart_item(id, g.current_user.id, data.get('quantity'))
        cart_data = get_cart(g.current_user.id)
        return success_response(cart_data, "Cart updated")
    except Exception as e:
        return error_response(str(e), 500)

@cart_bp.route('/items/<int:id>', methods=['DELETE'])
@login_required()
def delete_item(id):
    try:
        remove_cart_item(id, g.current_user.id)
        cart_data = get_cart(g.current_user.id)
        return success_response(cart_data, "Item removed")
    except Exception as e:
        return error_response(str(e), 500)

@cart_bp.route('/', methods=['DELETE'])
@login_required()
def empty_cart():
    try:
        clear_cart(g.current_user.id)
        return success_response(None, "Cart cleared")
    except Exception as e:
        return error_response(str(e), 500)
