# app/models/market_price.py
from datetime import datetime, timezone
from app import db

class MarketPrice(db.Model):
    __tablename__ = 'market_prices'

    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    average_price = db.Column(db.Numeric(10, 2), nullable=False)
    unit = db.Column(db.String(20), nullable=False, default='kg') # e.g., kg, 90kg bag, crate
    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<MarketPrice {self.crop_name}: {self.average_price}/{self.unit}>'