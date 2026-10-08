from app.models.user import User
from app.extensions import db

def register_user(name, email, password, phone=None):
    if not name or not email or not password or len(password.strip()) < 6:
        return None
    cleaned_email = email.strip().lower()
    if User.query.filter(User.email.ilike(cleaned_email)).first():
        return None
    user = User(name=name.strip(), email=cleaned_email, phone=phone.strip() if phone else None)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(email, password):
    if not email or not password:
        return None
    cleaned_email = email.strip().lower()
    user = User.query.filter(User.email.ilike(cleaned_email)).first()
    if user and user.check_password(password) and user.is_active:
        return user
    return None

def update_profile(user, data):
    if 'name' in data and data['name']:
        user.name = data['name'].strip()
    if 'phone' in data:
        user.phone = data['phone'].strip() if data['phone'] else None
    db.session.commit()
    return user

def change_password(user, current_password, new_password):
    if not current_password or not new_password or len(new_password.strip()) < 6:
        return False
    if user.check_password(current_password):
        user.set_password(new_password)
        db.session.commit()
        return True
    return False
