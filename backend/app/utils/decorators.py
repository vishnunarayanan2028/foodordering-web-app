from functools import wraps
from flask import g
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db
from .helpers import error_response

def login_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.session.get(User, user_id)
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
            user = db.session.get(User, user_id)
            if not user:
                return error_response("User not found", 401)
            g.current_user = user
            if user.role not in roles:
                return error_response("Forbidden: insufficient permissions", 403)
            return fn(*args, **kwargs)
        return decorator
    return wrapper

