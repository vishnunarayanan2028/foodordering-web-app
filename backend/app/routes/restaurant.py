from flask import Blueprint, request
from app.models.restaurant import Restaurant
from app.services.order_service import get_restaurant_orders, update_order_status, get_dashboard_stats
from app.utils.helpers import success_response, error_response
from app.utils.decorators import role_required
from app.extensions import db

restaurant_bp = Blueprint('restaurant_bp', __name__, url_prefix='/api/restaurant')

@restaurant_bp.route('/', methods=['GET'])
@restaurant_bp.route('/all', methods=['GET'])
def list_restaurants():
    try:
        restaurants = Restaurant.query.filter_by(is_active=True).all()
        return success_response([r.to_dict() for r in restaurants])
    except Exception as e:
        return error_response(str(e), 500)

@restaurant_bp.route('/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    try:
        r = db.session.get(Restaurant, id)
        if r:
            return success_response(r.to_dict())
        return error_response("Restaurant not found", 404)
    except Exception as e:
        return error_response(str(e), 500)


@restaurant_bp.route('/', methods=['PUT'])
@role_required('restaurant', 'admin')
def update_restaurant():
    data = request.get_json()
    try:
        r = Restaurant.query.first()
        if r:
            for key, value in data.items():
                if hasattr(r, key) and key not in ['id', 'owner_id', 'created_at']:
                    setattr(r, key, value)
            db.session.commit()
            return success_response(r.to_dict(), "Restaurant updated")
        return error_response("Not found", 404)
    except Exception as e:
        return error_response(str(e), 500)

@restaurant_bp.route('/orders', methods=['GET'])
@role_required('restaurant', 'admin')
def list_restaurant_orders():
    filters = {'status': request.args.get('status')}
    try:
        r = Restaurant.query.first()
        orders = get_restaurant_orders(r.id, filters)
        return success_response([o.to_dict() for o in orders])
    except Exception as e:
        return error_response(str(e), 500)

@restaurant_bp.route('/orders/<int:id>/status', methods=['PUT'])
@role_required('restaurant', 'admin')
def change_order_status(id):
    data = request.get_json()
    try:
        order = update_order_status(id, data.get('status'))
        if order:
            return success_response(order.to_dict(), "Status updated")
        return error_response("Order not found", 404)
    except Exception as e:
        return error_response(str(e), 500)

@restaurant_bp.route('/dashboard', methods=['GET'])
@role_required('restaurant', 'admin')
def restaurant_dashboard():
    try:
        r = Restaurant.query.first()
        stats = get_dashboard_stats(r.id)
        return success_response(stats)
    except Exception as e:
        return error_response(str(e), 500)
