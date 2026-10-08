from app.models.cart import CartItem
from app.models.food import Food
from app.extensions import db

def get_cart(user_id):
    items = CartItem.query.filter_by(user_id=user_id).all()
    subtotal = 0.0
    items_data = []
    for item in items:
        food = item.food
        if food:
            item_subtotal = float(food.price) * item.quantity
            subtotal += item_subtotal
            item_dict = item.to_dict()
            item_dict['item_subtotal'] = item_subtotal
            items_data.append(item_dict)
    
    return {
        'items': items_data,
        'cart_subtotal': subtotal,
        'tax': subtotal * 0.05,
        'delivery_fee': 40.0 if items else 0.0,
        'total': subtotal + (subtotal * 0.05) + (40.0 if items else 0.0)
    }

def add_to_cart(user_id, food_id, quantity=1):
    food_to_add = db.session.get(Food, food_id)
    if not food_to_add:
        raise ValueError("Food item not found")

    existing_items = CartItem.query.filter_by(user_id=user_id).all()
    if existing_items:
        first_restaurant_id = existing_items[0].food.restaurant_id
        if first_restaurant_id != food_to_add.restaurant_id:
            raise ValueError("Your cart contains items from another restaurant. Please clear your cart first.")

    item = CartItem.query.filter_by(user_id=user_id, food_id=food_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(user_id=user_id, food_id=food_id, quantity=quantity)
        db.session.add(item)
    db.session.commit()
    return item


def update_cart_item(item_id, user_id, quantity):
    item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
    if item:
        if quantity <= 0:
            db.session.delete(item)
        else:
            item.quantity = quantity
        db.session.commit()
    return item

def remove_cart_item(item_id, user_id):
    item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return True
    return False

def clear_cart(user_id):
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()
