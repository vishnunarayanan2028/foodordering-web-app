from flask import Blueprint, request, g
from app.services.order_service import create_order, get_user_orders, get_order_detail, cancel_order
from app.utils.helpers import success_response, error_response
from app.utils.decorators import login_required

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@orders_bp.route('/', methods=['POST'])
@login_required()
def place_order():
    data = request.get_json()
    try:
        order = create_order(g.current_user.id, data)
        return success_response(order.to_dict(), "Order placed", 201)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)

@orders_bp.route('/', methods=['GET'])
@login_required()
def list_orders():
    try:
        orders = get_user_orders(g.current_user.id)
        return success_response([o.to_dict() for o in orders], "Orders retrieved")
    except Exception as e:
        return error_response(str(e), 500)

@orders_bp.route('/<int:id>', methods=['GET'])
@login_required()
def order_detail(id):
    try:
        order = get_order_detail(id, g.current_user.id)
        if order:
            data = order.to_dict()
            data['items'] = [i.to_dict() for i in order.items]
            return success_response(data, "Order detail retrieved")
        return error_response("Order not found", 404)
    except Exception as e:
        return error_response(str(e), 500)

@orders_bp.route('/<int:id>/cancel', methods=['PUT'])
@login_required()
def order_cancel(id):
    try:
        success = cancel_order(id, g.current_user.id)
        if success:
            return success_response(None, "Order cancelled")
        return error_response("Cannot cancel order", 400)
    except Exception as e:
        return error_response(str(e), 500)
