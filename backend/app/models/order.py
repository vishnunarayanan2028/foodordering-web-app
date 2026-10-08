from datetime import datetime, timezone
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
            'restaurant_name': self.restaurant.name if hasattr(self, 'restaurant') and self.restaurant else 'Madurai Hotel',
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
            'status': self.order_status,

            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
