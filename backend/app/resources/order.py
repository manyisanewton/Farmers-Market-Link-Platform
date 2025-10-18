# app/resources/order.py
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from decimal import Decimal

from app.services.twilio_service import send_sms
from app.utils.decorators import buyer_required, farmer_required
from app.models.user import User
from app.models.produce import Produce
from app.models.order import Order, OrderItem
from app.schemas.order import OrderSchema
from app import db

order_bp = Blueprint('order_bp', __name__)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@order_bp.route('/', methods=['POST'])
@jwt_required()
@buyer_required
def create_order():
    """
    Create a new order
    ---
    tags:
      - Orders
    summary: Create a new order (Buyer Only)
    description: Allows a logged-in buyer to create a new order by providing a list of produce items and their quantities.
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [items]
            properties:
              items:
                type: array
                description: A list of items to include in the order.
                items:
                  type: object
                  required: [produce_id, quantity]
                  properties:
                    produce_id: { type: integer, example: 1 }
                    quantity: { type: integer, example: 5 }
    responses:
      '201':
        description: Order created successfully.
      '400':
        description: Bad Request. E.g., insufficient stock for an item.
      '403':
        description: Forbidden. User is not a buyer.
    """
    json_data = request.get_json()
    buyer_id = int(get_jwt_identity())
    try:
        data = order_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    total_price = Decimal('0.0')
    order_items_to_create = []
    new_order = None
    try:
        with db.session.begin_nested():
            for item_data in data['items']:
                produce_item = db.session.get(Produce, item_data['produce_id'])
                if not produce_item:
                    return jsonify(message=f"Produce with id {item_data['produce_id']} not found."), 404
                if produce_item.quantity < item_data['quantity']:
                    return jsonify(message=f"Insufficient stock for {produce_item.name}. Available: {produce_item.quantity}"), 400
                produce_item.quantity -= item_data['quantity']
                price_for_item = produce_item.price * Decimal(str(item_data['quantity']))
                total_price += price_for_item
                order_items_to_create.append(OrderItem(
                    produce_id=produce_item.id,
                    quantity=item_data['quantity'],
                    price_per_unit=produce_item.price
                ))
            new_order = Order(buyer_id=buyer_id, total_price=total_price)
            new_order.items.extend(order_items_to_create)
            db.session.add(new_order)
        db.session.commit()
        db.session.refresh(new_order)
        buyer = db.session.get(User, buyer_id)
        farmer_ids = {item.produce.farmer_id for item in new_order.items}
        for farmer_id in farmer_ids:
            farmer = db.session.get(User, farmer_id)
            if farmer and farmer.phone_number:
                message = f"Hello {farmer.username}, you've received a new order from {buyer.username}. Log in to confirm."
                send_sms(farmer.phone_number, message)
    except Exception as e:
        db.session.rollback()
        return jsonify(message="An error occurred while creating the order.", error=str(e)), 500
    return jsonify(order_schema.dump(new_order)), 201

@order_bp.route('/', methods=['GET'])
@jwt_required()
@buyer_required
def get_buyer_orders():
    """
    Get my orders (as a Buyer)
    ---
    tags:
      - Orders
    summary: Get my orders (as a Buyer)
    description: Retrieves a list of all orders placed by the currently authenticated buyer.
    security:
      - bearerAuth: []
    responses:
      '200':
        description: A list of the buyer's orders.
    """
    buyer_id = int(get_jwt_identity())
    orders = Order.query.filter_by(buyer_id=buyer_id).order_by(Order.created_at.desc()).all()
    return jsonify(orders_schema.dump(orders)), 200

@order_bp.route('/farmer', methods=['GET'])
@jwt_required()
@farmer_required
def get_farmer_orders():
    """
    Get incoming orders (as a Farmer)
    ---
    tags:
      - Orders
    summary: Get incoming orders (as a Farmer)
    description: Retrieves a list of all orders that contain at least one produce item belonging to the currently authenticated farmer.
    security:
      - bearerAuth: []
    responses:
      '200':
        description: A list of the farmer's relevant orders.
    """
    farmer_id = int(get_jwt_identity())
    orders = Order.query.join(OrderItem).join(Produce).filter(
        Produce.farmer_id == farmer_id
    ).distinct().order_by(Order.created_at.desc()).all()
    return jsonify(orders_schema.dump(orders)), 200

@order_bp.route('/<int:order_id>', methods=['PATCH'])
@jwt_required()
@farmer_required
def update_order_status(order_id):
    """
    Update an order's status
    ---
    tags:
      - Orders
    summary: Update an order's status (Farmer Only)
    description: Allows a farmer who owns produce within an order to update the status of that order.
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: order_id
        required: true
        schema: { type: integer }
        description: The ID of the order to update.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [status]
            properties:
              status:
                type: string
                enum: [Confirmed, Delivered, Canceled]
                example: Confirmed
    responses:
      '200':
        description: Order status updated successfully.
      '400':
        description: Invalid status provided.
      '403':
        description: Forbidden. User is not an authorized farmer for this order.
      '404':
        description: Not Found. Order not found or user does not have permission.
    """
    farmer_id = int(get_jwt_identity())
    order = Order.query.join(OrderItem).join(Produce).filter(
        Order.id == order_id,
        Produce.farmer_id == farmer_id
    ).first_or_404(description="Order not found or you do not have permission to modify it.")
    json_data = request.get_json()
    new_status = json_data.get('status')
    if not new_status or new_status not in ['Confirmed', 'Delivered', 'Canceled']:
        return jsonify(message="Invalid status provided. Must be one of: Confirmed, Delivered, Canceled."), 400
    order.status = new_status
    db.session.commit()
    return jsonify(order_schema.dump(order)), 200