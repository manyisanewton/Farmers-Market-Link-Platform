# app/models/transaction.py
from datetime import datetime, timezone
from app import db

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    mpesa_receipt_number = db.Column(db.String(50), nullable=True, unique=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending') # Pending, Success, Failed
    checkout_request_id = db.Column(db.String(100), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    # Foreign Key to the Order
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)

    def __repr__(self):
        return f'<Transaction {self.mpesa_receipt_number}>'