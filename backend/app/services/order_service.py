from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.cart import CartItem
from app.models.restaurant import Restaurant
from app.models.user import User
from app.utils.helpers import generate_order_number
from app.extensions import db

def create_order(user_id, data):
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        raise ValueError("Cart is empty")
    
    restaurant_id = cart_items[0].food.restaurant_id
    subtotal = sum(float(item.food.price) * item.quantity for item in cart_items)
    tax = subtotal * 0.05
    delivery_fee = 40.0
    discount = data.get('discount', 0)
    total_amount = subtotal + tax + delivery_fee - discount

    pay_method = data.get('payment_method', 'cash_on_delivery')
    pay_status = 'paid' if pay_method.lower() in ['demo_payment', 'card', 'upi', 'online'] else 'pending'

    order = Order(
        order_number=generate_order_number(),
        customer_id=user_id,
        restaurant_id=restaurant_id,
        subtotal=subtotal,
        tax=tax,
        delivery_fee=delivery_fee,
        discount=discount,
        total_amount=total_amount,
        delivery_address=data['delivery_address'],
        phone=data['phone'],
        payment_method=pay_method,
        payment_status=pay_status,
        notes=data.get('notes')
    )

    db.session.add(order)
    db.session.flush()

    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            food_id=item.food_id,
            food_name_snapshot=item.food.name,
            price_snapshot=item.food.price,
            quantity=item.quantity,
            subtotal=float(item.food.price) * item.quantity
        )
        db.session.add(order_item)
        db.session.delete(item)

    db.session.commit()
    return order

def get_user_orders(user_id):
    return Order.query.filter_by(customer_id=user_id).order_by(Order.created_at.desc()).all()

def get_order_detail(order_id, user_id):
    return Order.query.filter_by(id=order_id, customer_id=user_id).first()

def cancel_order(order_id, user_id):
    order = Order.query.filter_by(id=order_id, customer_id=user_id).first()
    if order and order.order_status == 'placed':
        order.order_status = 'cancelled'
        db.session.commit()
        return True
    return False

def get_restaurant_orders(restaurant_id, filters):
    query = Order.query.filter_by(restaurant_id=restaurant_id)
    if filters.get('status'):
        query = query.filter_by(order_status=filters['status'])
    return query.order_by(Order.created_at.desc()).all()

def update_order_status(order_id, new_status):
    order = db.session.get(Order, order_id)
    if order:
        order.order_status = new_status
        db.session.commit()
        return order
    return None

def get_dashboard_stats(restaurant_id):
    orders = Order.query.filter_by(restaurant_id=restaurant_id).all()
    total_revenue = sum(float(o.total_amount) for o in orders if o.order_status == 'delivered')
    pending = len([o for o in orders if o.order_status in ['placed', 'confirmed', 'preparing']])
    import datetime
    today = datetime.date.today()
    today_orders = len([o for o in orders if o.created_at.date() == today])
    return {
        'total_orders': len(orders),
        'total_revenue': total_revenue,
        'pending_orders': pending,
        'today_orders': today_orders
    }

def get_admin_stats():
    orders = Order.query.all()
    users = User.query.all()
    total_revenue = sum(float(o.total_amount) for o in orders if o.order_status == 'delivered')
    return {
        'total_users': len(users),
        'total_orders': len(orders),
        'total_revenue': total_revenue
    }
