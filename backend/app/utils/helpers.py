import datetime
from flask import jsonify
from app.extensions import db
from app.models.order import Order

def generate_order_number():
    today = datetime.date.today()
    date_str = today.strftime("%Y%m%d")
    
    # Get count of orders today
    count = Order.query.filter(db.func.date(Order.created_at) == today).count()
    next_num = count + 1
    
    return f"FM-{date_str}-{next_num:04d}"

def success_response(data=None, message='Success', status_code=200):
    return jsonify({
        'status': 'success',
        'message': message,
        'data': data
    }), status_code

def error_response(message='Error', status_code=400):
    return jsonify({
        'status': 'error',
        'message': message
    }), status_code
