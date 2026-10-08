from .auth import auth_bp
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
