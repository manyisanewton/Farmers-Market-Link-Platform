# app/resources/produce.py
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
import cloudinary.uploader

from app.models.produce import Produce
from app.schemas.produce import ProduceSchema
from app.utils.decorators import farmer_required
from app import db

produce_bp = Blueprint('produce_bp', __name__)
produce_schema = ProduceSchema()
produces_schema = ProduceSchema(many=True)

@produce_bp.route('/', methods=['POST'])
@jwt_required()
@farmer_required
def create_produce():
    """
    Create a new produce listing
    ---
    tags:
      - Produce
    summary: Create a new produce listing (Farmer Only)
    description: Allows an approved farmer to add a new produce item to the marketplace. This endpoint handles image uploads via multipart/form-data.
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        multipart/form-data:
          schema:
            type: object
            required: [name, price, quantity, unit]
            properties:
              name: { type: string, example: "Fresh Tomatoes" }
              description: { type: string, example: "Organically grown in Nakuru." }
              price: { type: number, format: float, example: 85.50 }
              quantity: { type: integer, example: 50 }
              unit: { type: string, enum: [kg, bunch, crate, item], example: "kg" }
              location: { type: string, example: "Nakuru" }
              image: { type: string, format: binary, description: "Optional image file for the produce." }
    responses:
      '201':
        description: Produce created successfully.
      '403':
        description: Forbidden. User is not an approved farmer.
      '422':
        description: Unprocessable Entity. Validation error on form data.
    """
    farmer_id = get_jwt_identity()
    form_data = request.form.to_dict()
    
    try:
        data = produce_schema.load(form_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    image_url = None
    if 'image' in request.files:
        image_file = request.files['image']
        try:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder="fmlp_produce_images"
            )
            image_url = upload_result.get('secure_url')
        except Exception as e:
            return jsonify(message="Image upload failed.", error=str(e)), 500

    new_produce = Produce(
        farmer_id=int(farmer_id),
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        quantity=data['quantity'],
        unit=data['unit'],
        location=data.get('location'),
        image_url=image_url
    )
    
    db.session.add(new_produce)
    db.session.commit()
    
    return jsonify(produce_schema.dump(new_produce)), 201

@produce_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_produce():
    """
    Get all available produce
    ---
    tags:
      - Produce
    summary: Get all available produce listings
    description: Retrieves a list of all available produce, with optional filtering. Accessible by any authenticated user.
    security:
      - bearerAuth: []
    parameters:
      - in: query
        name: name
        schema: { type: string }
        description: Filter by produce name (case-insensitive, partial match).
      - in: query
        name: location
        schema: { type: string }
        description: Filter by location/county (case-insensitive, partial match).
      - in: query
        name: min_price
        schema: { type: number, format: float }
        description: Filter for items with a price greater than or equal to this value.
      - in: query
        name: max_price
        schema: { type: number, format: float }
        description: Filter for items with a price less than or equal to this value.
    responses:
      '200':
        description: A list of produce items.
    """
    query = Produce.query.filter_by(is_available=True)
    produce_name = request.args.get('name')
    if produce_name:
        query = query.filter(Produce.name.ilike(f"%{produce_name}%"))
    location = request.args.get('location')
    if location:
        query = query.filter(Produce.location.ilike(f"%{location}%"))
    min_price = request.args.get('min_price', type=float)
    if min_price is not None:
        query = query.filter(Produce.price >= min_price)
    max_price = request.args.get('max_price', type=float)
    if max_price is not None:
        query = query.filter(Produce.price <= max_price)
    all_produce = query.order_by(Produce.created_at.desc()).all()
    return jsonify(produces_schema.dump(all_produce)), 200

@produce_bp.route('/<int:produce_id>', methods=['PUT'])
@jwt_required()
@farmer_required
def update_produce(produce_id):
    """
    Update a produce listing
    ---
    tags:
      - Produce
    summary: Update a produce listing (Owner Only)
    description: Allows a farmer to update the details of their own produce listing.
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: produce_id
        required: true
        schema: { type: integer }
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              price: { type: number, format: float }
              quantity: { type: integer }
              description: { type: string }
              location: { type: string }
    responses:
      '200':
        description: Produce updated successfully.
      '403':
        description: Forbidden. User does not own this listing.
    """
    produce = db.get_or_404(Produce, produce_id)
    farmer_id_from_token = get_jwt_identity()
    if produce.farmer_id != int(farmer_id_from_token):
        return jsonify(message="Unauthorized: You do not own this listing"), 403
    json_data = request.get_json()
    try:
        data = produce_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 422
    for key, value in data.items():
        setattr(produce, key, value)
    db.session.commit()
    return jsonify(produce_schema.dump(produce)), 200

@produce_bp.route('/<int:produce_id>', methods=['DELETE'])
@jwt_required()
@farmer_required
def delete_produce(produce_id):
    """
    Delete a produce listing
    ---
    tags:
      - Produce
    summary: Delete a produce listing (Owner Only)
    description: Allows a farmer to delete their own produce listing.
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: produce_id
        required: true
        schema: { type: integer }
    responses:
      '204':
        description: Produce deleted successfully. No content returned.
      '403':
        description: Forbidden. User does not own this listing.
    """
    produce = db.get_or_404(Produce, produce_id)
    farmer_id_from_token = get_jwt_identity()
    if produce.farmer_id != int(farmer_id_from_token):
        return jsonify(message="Unauthorized: You do not own this listing"), 403
    db.session.delete(produce)
    db.session.commit()
    return '', 204