import os

base_dir = r"e:\Foodbooking\backend"

files_to_create = {
    "requirements.txt": """Flask==3.1.3
Flask-SQLAlchemy==3.1.1
Flask-CORS==5.0.1
flask-jwt-extended==4.7.1
mysql-connector-python==9.1.0
python-dotenv==1.1.0
pytest==8.3.4
""",
    ".env.example": """FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this
DATABASE_URL=mysql+mysqlconnector://root:@localhost/foodmunch_db
""",
    "run.py": """from dotenv import load_dotenv
load_dotenv()

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
""",
    "README.md": """# Food Munch Backend

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set up MySQL database: `CREATE DATABASE foodmunch_db;`
3. Configure `.env` from `.env.example`
4. Seed database: `python seed.py`
5. Run server: `python run.py`
6. Run tests: `pytest`
""",
    "app/__init__.py": """import os
from flask import Flask, send_from_directory
from .config import Config
from .extensions import db, jwt, cors
from .routes import register_blueprints

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    register_blueprints(app)

    # Compute frontend_dir as the absolute path to e:\\Foodbooking\\frontend
    frontend_dir = os.path.abspath(os.path.join(app.root_path, '..', '..', 'frontend'))

    @app.route('/')
    def index():
        return send_from_directory(frontend_dir, 'index.html')

    @app.route('/<path:path>')
    def serve_frontend(path):
        if path.startswith('api/'):
            return "Not Found", 404
        if os.path.exists(os.path.join(frontend_dir, path)):
            return send_from_directory(frontend_dir, path)
        elif os.path.exists(os.path.join(frontend_dir, path + '.html')):
            return send_from_directory(frontend_dir, path + '.html')
        else:
            return send_from_directory(frontend_dir, 'index.html')

    return app
""",
    "app/config.py": """import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://root:@localhost/foodmunch_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key-change-this'
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours in seconds
""",
    "app/extensions.py": """from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
""",
    "app/models/__init__.py": """from .user import User
from .restaurant import Restaurant
from .category import Category
from .food import Food
from .cart import CartItem
from .order import Order
from .order_item import OrderItem
""",
    "app/models/user.py": """from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='customer')  # customer, restaurant, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='customer', lazy=True, foreign_keys='Order.customer_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
""",
    "app/models/restaurant.py": """from datetime import datetime, timezone
from app.extensions import db

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    categories = db.relationship('Category', backref='restaurant', lazy=True, cascade='all, delete-orphan')
    foods = db.relationship('Food', backref='restaurant', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='restaurant', lazy=True)
    owner = db.relationship('User', backref='restaurant', uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
""",
    "app/models/category.py": """from datetime import datetime, timezone
from app.extensions import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    foods = db.relationship('Food', backref='category', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'display_order': self.display_order,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
""",
    "app/models/food.py": """from datetime import datetime, timezone
from app.extensions import db

class Food(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    is_veg = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price) if self.price else 0.0,
            'image_url': self.image_url,
            'is_available': self.is_available,
            'is_veg': self.is_veg,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
""",
    "app/models/cart.py": """from datetime import datetime, timezone
from app.extensions import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    __table_args__ = (db.UniqueConstraint('user_id', 'food_id', name='uq_user_food'),)
    food = db.relationship('Food', backref='cart_items', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'food_id': self.food_id,
            'quantity': self.quantity,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'food': self.food.to_dict() if self.food else None
        }
""",
    "app/models/order.py": """from datetime import datetime, timezone
from app.extensions import db

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    tax = db.Column(db.Numeric(10, 2), default=0)
    delivery_fee = db.Column(db.Numeric(10, 2), default=0)
    discount = db.Column(db.Numeric(10, 2), default=0)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    delivery_address = db.Column(db.String(500), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    payment_method = db.Column(db.String(50), default='cash_on_delivery')
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    order_status = db.Column(db.String(30), default='placed')  # placed, confirmed, preparing, ready, out_for_delivery, delivered, cancelled
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'customer_id': self.customer_id,
            'restaurant_id': self.restaurant_id,
            'subtotal': float(self.subtotal) if self.subtotal is not None else 0.0,
            'tax': float(self.tax) if self.tax is not None else 0.0,
            'delivery_fee': float(self.delivery_fee) if self.delivery_fee is not None else 0.0,
            'discount': float(self.discount) if self.discount is not None else 0.0,
            'total_amount': float(self.total_amount) if self.total_amount is not None else 0.0,
            'delivery_address': self.delivery_address,
            'phone': self.phone,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'order_status': self.order_status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
""",
    "app/models/order_item.py": """from app.extensions import db

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=True)
    food_name_snapshot = db.Column(db.String(150), nullable=False)
    price_snapshot = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    food = db.relationship('Food', backref='order_items', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'food_id': self.food_id,
            'food_name_snapshot': self.food_name_snapshot,
            'price_snapshot': float(self.price_snapshot) if self.price_snapshot is not None else 0.0,
            'quantity': self.quantity,
            'subtotal': float(self.subtotal) if self.subtotal is not None else 0.0
        }
""",
    "app/utils/__init__.py": "",
    "app/utils/decorators.py": """from functools import wraps
from flask import g
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from .helpers import error_response

def login_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return error_response("User not found", 401)
            g.current_user = user
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return error_response("User not found", 401)
            g.current_user = user
            if user.role not in roles:
                return error_response("Forbidden: insufficient permissions", 403)
            return fn(*args, **kwargs)
        return decorator
    return wrapper
""",
    "app/utils/helpers.py": """import datetime
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
""",
    "app/routes/__init__.py": """from .auth import auth_bp
from .foods import foods_bp
from .categories import categories_bp
from .cart import cart_bp
from .orders import orders_bp
from .restaurant import restaurant_bp
from .admin import admin_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(foods_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(admin_bp)
""",
    "app/routes/auth.py": """from flask import Blueprint, request, g
from app.services.auth_service import register_user, authenticate_user, update_profile, change_password
from app.utils.helpers import success_response, error_response
from app.utils.decorators import login_required
from flask_jwt_extended import create_access_token
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user = register_user(data.get('name'), data.get('email'), data.get('password'), data.get('phone'))
        if not user:
            return error_response("Registration failed. Check if email is unique and password is >= 6 chars.", 400)
        access_token = create_access_token(identity=str(user.id))
        return success_response({
            'user': user.to_dict(),
            'token': access_token
        }, "Registration successful", 201)
    except Exception as e:
        return error_response(str(e), 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        user = authenticate_user(data.get('email'), data.get('password'))
        if not user:
            return error_response("Invalid credentials", 401)
        access_token = create_access_token(identity=str(user.id))
        return success_response({
            'user': user.to_dict(),
            'token': access_token
        }, "Login successful", 200)
    except Exception as e:
        return error_response(str(e), 500)

@auth_bp.route('/logout', methods=['POST'])
@login_required()
def logout():
    return success_response(None, "Logout successful", 200)

@auth_bp.route('/me', methods=['GET'])
@login_required()
def me():
    return success_response(g.current_user.to_dict(), "Profile retrieved", 200)

@auth_bp.route('/profile', methods=['PUT'])
@login_required()
def profile():
    data = request.get_json()
    try:
        updated_user = update_profile(g.current_user, data)
        return success_response(updated_user.to_dict(), "Profile updated", 200)
    except Exception as e:
        return error_response(str(e), 500)

@auth_bp.route('/password', methods=['PUT'])
@login_required()
def update_password():
    data = request.get_json()
    try:
        success = change_password(g.current_user, data.get('current_password'), data.get('new_password'))
        if success:
            return success_response(None, "Password updated successfully", 200)
        return error_response("Invalid current password", 400)
    except Exception as e:
        return error_response(str(e), 500)
""",
    "app/services/__init__.py": "",
    "app/services/auth_service.py": """from app.models.user import User
from app.extensions import db

def register_user(name, email, password, phone=None):
    if not email or not password or len(password) < 6:
        return None
    if User.query.filter_by(email=email).first():
        return None
    user = User(name=name, email=email, phone=phone)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password) and user.is_active:
        return user
    return None

def update_profile(user, data):
    if 'name' in data:
        user.name = data['name']
    if 'phone' in data:
        user.phone = data['phone']
    db.session.commit()
    return user

def change_password(user, current_password, new_password):
    if user.check_password(current_password):
        user.set_password(new_password)
        db.session.commit()
        return True
    return False
""",
    "app/routes/foods.py": """from flask import Blueprint, request
from app.services.food_service import get_foods, get_food_by_id, create_food, update_food, delete_food
from app.utils.helpers import success_response, error_response
from app.utils.decorators import role_required

foods_bp = Blueprint('foods', __name__, url_prefix='/api/foods')

@foods_bp.route('/', methods=['GET'])
def list_foods():
    filters = {
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
""",
    "app/services/food_service.py": """from app.models.food import Food
from app.models.category import Category
from app.models.restaurant import Restaurant
from app.extensions import db

def get_foods(filters):
    query = Food.query
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
    return Food.query.get(food_id)

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
    food = Food.query.get(food_id)
    if not food:
        return None
    for key, value in data.items():
        if hasattr(food, key) and key not in ['id', 'created_at', 'updated_at']:
            setattr(food, key, value)
    db.session.commit()
    return food

def delete_food(food_id):
    food = Food.query.get(food_id)
    if food:
        db.session.delete(food)
        db.session.commit()
        return True
    return False

def get_categories():
    return Category.query.filter_by(is_active=True).order_by(Category.display_order).all()

def get_category_by_id(category_id):
    return Category.query.get(category_id)

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
    category = Category.query.get(category_id)
    if not category:
        return None
    for key, value in data.items():
        if hasattr(category, key) and key not in ['id', 'created_at']:
            setattr(category, key, value)
    db.session.commit()
    return category

def delete_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return True
    return False
""",
    "app/routes/categories.py": """from flask import Blueprint, request
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
""",
    "app/routes/cart.py": """from flask import Blueprint, request, g
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
""",
    "app/services/cart_service.py": """from app.models.cart import CartItem
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
""",
    "app/routes/orders.py": """from flask import Blueprint, request, g
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
""",
    "app/services/order_service.py": """from app.models.order import Order
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
        payment_method=data.get('payment_method', 'cash_on_delivery'),
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
    order = Order.query.get(order_id)
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
""",
    "app/routes/restaurant.py": """from flask import Blueprint, request
from app.models.restaurant import Restaurant
from app.services.order_service import get_restaurant_orders, update_order_status, get_dashboard_stats
from app.utils.helpers import success_response, error_response
from app.utils.decorators import role_required
from app.extensions import db

restaurant_bp = Blueprint('restaurant_bp', __name__, url_prefix='/api/restaurant')

@restaurant_bp.route('/', methods=['GET'])
def get_restaurant():
    try:
        r = Restaurant.query.first()
        if r:
            return success_response(r.to_dict())
        return error_response("Not found", 404)
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
""",
    "app/routes/admin.py": """from flask import Blueprint, request
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
        user = User.query.get(id)
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
""",
    "seed.py": """from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.category import Category
from app.models.food import Food

app = create_app()

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        admin = User(name='Admin User', email='admin@demo.com', role='admin')
        admin.set_password('Demo@123')
        
        restaurant_user = User(name='Restaurant Owner', email='restaurant@demo.com', role='restaurant')
        restaurant_user.set_password('Demo@123')
        
        customer = User(name='John Customer', email='customer@demo.com', role='customer')
        customer.set_password('Demo@123')

        db.session.add_all([admin, restaurant_user, customer])
        db.session.commit()

        restaurant = Restaurant(
            owner_id=restaurant_user.id,
            name='Food Munch',
            address='123 Ayur Vigyan Nagar, New Delhi, India',
            email='orderfood@foodmunch.com'
        )
        db.session.add(restaurant)
        db.session.commit()

        categories_data = [
            {'name': 'Non-Veg Starters', 'image_url': 'https://d2clawv67efefq.cloudfront.net/ccbp-responsive-website/em-ginger-fried-img.png'},
            {'name': 'Veg Starters', 'image_url': 'https://d2clawv67efefq.cloudfront.net/ccbp-responsive-website/em-veg-starters-img.png'},
            {'name': 'Soups', 'image_url': 'https://d2clawv67efefq.cloudfront.net/ccbp-responsive-website/em-soup-img.png'},
            {'name': 'Fish & Seafood', 'image_url': 'https://d2clawv67efefq.cloudfront.net/ccbp-responsive-website/em-grilled-seafood-img.png'},
            {'name': 'Main Course', 'image_url': 'https://d2clawv67efefq.cloudfront.net/ccbp-responsive-website/em-hyderabadi-biryani-img.png'},
            {'name': 'Noodles', 'image_url': 'https://d2clawv67efefq.cloudfront.net/ccbp-responsive-website/em-mushroom-noodles-img.png'},
            {'name': 'Salads', 'image_url': 'https://d2clawv67efefq.cloudfront.net/ccbp-responsive-website/em-gluten-img.png'},
            {'name': 'Desserts', 'image_url': 'https://d2clawv67efefq.cloudfront.net/ccbp-responsive-website/em-coffee-bourbon-img.png'}
        ]

        categories = []
        for c in categories_data:
            cat = Category(restaurant_id=restaurant.id, name=c['name'], image_url=c['image_url'])
            categories.append(cat)
            db.session.add(cat)
        db.session.commit()

        for cat in categories:
            for i in range(3):
                food = Food(
                    restaurant_id=restaurant.id,
                    category_id=cat.id,
                    name=f"{cat.name} Item {i+1}",
                    description="Delicious and tasty food",
                    price=150.0 + i*50.0,
                    image_url=cat.image_url,
                    is_veg='Veg' in cat.name or 'Dessert' in cat.name
                )
                db.session.add(food)
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()
""",
    "tests/__init__.py": "",
    "tests/conftest.py": """import pytest
from app import create_app
from app.extensions import db
from app.models.user import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        user = User(name='Test Customer', email='test@example.com', role='customer')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
""",
    "tests/test_auth.py": """def test_register(client, app):
    response = client.post('/api/auth/register', json={
        'name': 'New User',
        'email': 'new@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201

def test_login(client, init_database):
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'token' in response.json['data']
""",
    "tests/test_foods.py": """def test_get_foods(client):
    response = client.get('/api/foods/')
    assert response.status_code == 200
""",
    "tests/test_cart.py": """def test_cart_empty(client, init_database):
    login_resp = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    token = login_resp.json['data']['token']
    
    response = client.get('/api/cart/', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
""",
    "tests/test_orders.py": """def test_get_orders(client, init_database):
    login_resp = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    token = login_resp.json['data']['token']
    
    response = client.get('/api/orders/', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
""",
    "tests/test_roles.py": """def test_customer_cannot_access_admin(client, init_database):
    login_resp = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    token = login_resp.json['data']['token']
    
    response = client.get('/api/admin/dashboard', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403
"""
}

for file_path, content in files_to_create.items():
    full_path = os.path.join(base_dir, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Created {len(files_to_create)} files successfully.")
