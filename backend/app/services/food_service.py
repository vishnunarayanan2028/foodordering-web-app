from app.models.food import Food
from app.models.category import Category
from app.models.restaurant import Restaurant
from app.extensions import db

def get_foods(filters):
    query = Food.query
    if filters.get('restaurant_id'):
        query = query.filter_by(restaurant_id=filters['restaurant_id'])
    if filters.get('category_id'):
        query = query.filter_by(category_id=filters['category_id'])

    if filters.get('search'):
        search = f"%{filters['search']}%"
        query = query.filter(Food.name.ilike(search) | Food.description.ilike(search))
    if filters.get('is_veg') is not None:
        is_veg = str(filters['is_veg']).lower() == 'true'
        query = query.filter_by(is_veg=is_veg)
    if filters.get('is_available') is not None:
        query = query.filter_by(is_available=filters['is_available'])
    
    return query.all()

def get_food_by_id(food_id):
    return db.session.get(Food, food_id)

def create_food(data):
    # Auto-set restaurant_id to first restaurant if not provided
    if 'restaurant_id' not in data:
        restaurant = Restaurant.query.first()
        if restaurant:
            data['restaurant_id'] = restaurant.id
        else:
            raise ValueError("No restaurant exists")
            
    food = Food(
        restaurant_id=data['restaurant_id'],
        category_id=data['category_id'],
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        image_url=data.get('image_url'),
        is_veg=data.get('is_veg', False),
        is_available=data.get('is_available', True)
    )
    db.session.add(food)
    db.session.commit()
    return food

def update_food(food_id, data):
    food = db.session.get(Food, food_id)
    if not food:
        return None
    for key, value in data.items():
        if hasattr(food, key) and key not in ['id', 'created_at', 'updated_at']:
            setattr(food, key, value)
    db.session.commit()
    return food

def delete_food(food_id):
    food = db.session.get(Food, food_id)
    if food:
        db.session.delete(food)
        db.session.commit()
        return True
    return False

def get_categories():
    return Category.query.filter_by(is_active=True).order_by(Category.display_order).all()

def get_category_by_id(category_id):
    return db.session.get(Category, category_id)

def create_category(data):
    if 'restaurant_id' not in data:
        restaurant = Restaurant.query.first()
        if restaurant:
            data['restaurant_id'] = restaurant.id
        else:
            raise ValueError("No restaurant exists")
    category = Category(
        restaurant_id=data['restaurant_id'],
        name=data['name'],
        description=data.get('description'),
        image_url=data.get('image_url')
    )
    db.session.add(category)
    db.session.commit()
    return category

def update_category(category_id, data):
    category = db.session.get(Category, category_id)
    if not category:
        return None
    for key, value in data.items():
        if hasattr(category, key) and key not in ['id', 'created_at']:
            setattr(category, key, value)
    db.session.commit()
    return category

def delete_category(category_id):
    category = db.session.get(Category, category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return True
    return False
