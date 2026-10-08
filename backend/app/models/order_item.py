from app.extensions import db

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
        food_data = self.food.to_dict() if self.food else {
            'name': self.food_name_snapshot,
            'price': float(self.price_snapshot) if self.price_snapshot is not None else 0.0,
            'image_url': '/images/em-veg-starters-img.png'
        }
        return {
            'id': self.id,
            'order_id': self.order_id,
            'food_id': self.food_id,
            'food_name_snapshot': self.food_name_snapshot,
            'price_snapshot': float(self.price_snapshot) if self.price_snapshot is not None else 0.0,
            'price': float(self.price_snapshot) if self.price_snapshot is not None else 0.0,
            'quantity': self.quantity,
            'subtotal': float(self.subtotal) if self.subtotal is not None else 0.0,
            'food': food_data
        }

