# app/models/produce.py
from datetime import datetime, timezone
from app import db

class Produce(db.Model):
    __tablename__ = 'produce'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False,index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(20), nullable=False, default='kg')
    image_url = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(100), nullable=True, index=True)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    
    # Use timezone-aware datetime objects
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    def __repr__(self):
        return f'<Produce {self.name}>'