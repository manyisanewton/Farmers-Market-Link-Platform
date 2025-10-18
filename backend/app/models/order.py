# app/models/order.py
from datetime import datetime, timezone
from app import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False, default='Pending') # e.g., Pending, Confirmed, Delivered, Canceled
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")
    transaction = db.relationship('Transaction', backref='order', uselist=False, lazy=True, cascade="all, delete-orphan")
    def __repr__(self):
        return f'<Order {self.id}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.Numeric(10, 2), nullable=False) # Price at the time of order

    # Foreign Keys
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    produce_id = db.Column(db.Integer, db.ForeignKey('produce.id'), nullable=False)

    # Relationship to get produce details
    produce = db.relationship('Produce', backref='order_items')

    def __repr__(self):
        return f'<OrderItem Order:{self.order_id} Produce:{self.produce_id}>'