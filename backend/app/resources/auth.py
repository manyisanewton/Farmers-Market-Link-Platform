# app/resources/auth.py
from flask import request, jsonify, Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required
from app.models.user import User
from app.schemas.user import UserSchema
from app import db

auth_bp = Blueprint('auth_bp', __name__)
user_schema = UserSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    summary: Register a new user (Farmer or Buyer)
    description: Creates a new user account. Farmers are created with an unapproved status by default.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [username, email, password, role, phone_number]
            properties:
              username:
                type: string
                example: jdoe_farmer
              email:
                type: string
                format: email
                example: "john.doe@fmlp.com"
              password:
                type: string
                format: password
                example: secureP@ss123
              role:
                type: string
                enum: [farmer, buyer]
                example: farmer
              phone_number:
                type: string
                example: "+254712345678"
    responses:
      '201':
        description: User created successfully.
      '409':
        description: Conflict. Username or email already exists.
      '422':
        description: Unprocessable Entity. Validation error.
    """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists"}), 409

    user = User(
        username=data['username'],
        email=data['email'],
        role=data['role'],
        phone_number=data.get('phone_number')
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Log in a user
    ---
    tags:
      - Authentication
    summary: Log in and get JWT tokens
    description: Authenticates user credentials and returns access and refresh tokens.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [email, password]
            properties:
              email:
                type: string
                format: email
                example: "john.doe@fmlp.com"
              password:
                type: string
                format: password
                example: secureP@ss123
    responses:
      '200':
        description: Successful login, returns tokens.
      '401':
        description: Invalid credentials.
    """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    email = json_data.get('email', None)
    password = json_data.get('password', None)

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        identity = str(user.id)
        access_token = create_access_token(identity=identity, fresh=True)
        refresh_token = create_refresh_token(identity=identity)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200

    return jsonify({"message": "Invalid credentials"}), 401

  