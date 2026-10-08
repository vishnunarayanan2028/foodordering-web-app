import os
from urllib.parse import urlparse
from flask import Flask, send_from_directory
from .config import Config
from .extensions import db, jwt, cors
from .routes import register_blueprints

def ensure_database_exists(db_url):
    try:
        parsed = urlparse(db_url)
        username = parsed.username or 'root'
        password = parsed.password or ''
        host = parsed.hostname or 'localhost'
        port = parsed.port or 3306
        dbname = parsed.path.lstrip('/') or 'foodmunch_db'

        import mysql.connector
        conn = mysql.connector.connect(host=host, port=port, user=username, password=password)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.close()
    except Exception as e:
        print(f"[Notice] Database auto-create skipped or check failed: {e}")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.url_map.strict_slashes = False

    ensure_database_exists(app.config.get('SQLALCHEMY_DATABASE_URI', ''))

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    with app.app_context():
        from .models import user, restaurant, category, food, cart, order, order_item  # noqa: F401
        try:
            db.create_all()
            from .models.restaurant import Restaurant
            if Restaurant.query.count() == 0:
                print("[Setup] Seeding initial database records...")
                from seed import seed_data
                seed_data()
        except Exception as e:
            print(f"[Notice] db.create_all / seed notice: {e}")

    register_blueprints(app)

    # Compute frontend_dir as the absolute path to e:\Foodbooking\frontend
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
