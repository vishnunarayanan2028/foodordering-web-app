from datetime import datetime, timezone
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
    rating = db.Column(db.Float, default=4.5)
    cuisine = db.Column(db.String(100), default='South Indian / Madurai Special')
    city = db.Column(db.String(100), default='Madurai')
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
            'rating': self.rating or 4.5,
            'cuisine': self.cuisine or 'South Indian',
            'city': self.city or 'Madurai',
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

