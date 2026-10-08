from flask import Blueprint, request, g
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
