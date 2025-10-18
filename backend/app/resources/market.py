# app/resources/market.py
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.models.market_price import MarketPrice
from app.schemas.market_price import MarketPriceSchema
from app.utils.decorators import admin_required
from app import db

market_bp = Blueprint('market_bp', __name__)
market_price_schema = MarketPriceSchema()
market_prices_schema = MarketPriceSchema(many=True)

@market_bp.route('/prices', methods=['GET'])
@jwt_required()
def get_prices():
    """
    Get market price information
    ---
    tags:
      - Market
    summary: Get a list of all current market prices
    description: Retrieves a list of the current average market prices for various crops. Accessible by any authenticated user.
    security:
      - bearerAuth: []
    responses:
      '200':
        description: A list of current market prices.
    """
    prices = MarketPrice.query.order_by(MarketPrice.crop_name).all()
    return jsonify(market_prices_schema.dump(prices)), 200

@market_bp.route('/prices', methods=['POST'])
@jwt_required()
@admin_required
def create_price():
    """
    Create a new market price entry
    ---
    tags:
      - Market
    summary: Create a new market price entry (Admin Only)
    description: Allows a logged-in admin to add a new market price for a crop.
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [crop_name, average_price, unit]
            properties:
              crop_name:
                type: string
                example: Tomatoes
              average_price:
                type: string
                format: decimal
                example: "82.00"
              unit:
                type: string
                example: kg
    responses:
      '201':
        description: Market price created successfully.
      '403':
        description: Forbidden. User is not an admin.
      '409':
        description: Conflict. A price for this crop already exists.
    """
    json_data = request.get_json()
    try:
        data = market_price_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    if MarketPrice.query.filter_by(crop_name=data['crop_name']).first():
        return jsonify(message=f"A price for {data['crop_name']} already exists. Please update it instead."), 409

    new_price = MarketPrice(
        crop_name=data['crop_name'],
        average_price=data['average_price'],
        unit=data['unit']
    )
    db.session.add(new_price)
    db.session.commit()
    
    return jsonify(market_price_schema.dump(new_price)), 201