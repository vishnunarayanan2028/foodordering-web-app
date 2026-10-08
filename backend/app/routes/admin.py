from flask import Blueprint, request
from app.services.order_service import get_admin_stats
from app.models.user import User
from app.models.order import Order
from app.extensions import db
from app.utils.helpers import success_response, error_response
from app.utils.decorators import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/dashboard', methods=['GET'])
@role_required('admin')
def dashboard():
    try:
        stats = get_admin_stats()
        return success_response(stats)
    except Exception as e:
        return error_response(str(e), 500)

@admin_bp.route('/users', methods=['GET'])
@role_required('admin')
def list_users():
    try:
        users = User.query.all()
        return success_response([u.to_dict() for u in users])
    except Exception as e:
        return error_response(str(e), 500)

@admin_bp.route('/users/<int:id>', methods=['PUT'])
@role_required('admin')
def update_user(id):
    data = request.get_json()
    try:
        user = db.session.get(User, id)
        if user:
            if 'role' in data:
                user.role = data['role']
            if 'is_active' in data:
                user.is_active = data['is_active']
            db.session.commit()
            return success_response(user.to_dict(), "User updated")
        return error_response("User not found", 404)
    except Exception as e:
        return error_response(str(e), 500)

@admin_bp.route('/orders', methods=['GET'])
@role_required('admin')
def list_all_orders():
    try:
        orders = Order.query.all()
        return success_response([o.to_dict() for o in orders])
    except Exception as e:
        return error_response(str(e), 500)
