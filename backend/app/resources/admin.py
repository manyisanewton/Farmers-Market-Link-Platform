# app/resources/admin.py
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required

from marshmallow import ValidationError
from app.models.user import User
from app.schemas.user import UserSchema, AdminUserUpdateSchema
from app.utils.decorators import admin_required
from app import db

admin_bp = Blueprint('admin_bp', __name__)
users_schema = UserSchema(many=True)
user_schema = UserSchema()
user_update_schema = AdminUserUpdateSchema()

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    """
    Get all users
    ---
    tags:
      - Admin
    summary: Get a list of all users (Admin Only)
    description: Retrieves a complete list of all users registered on the platform. Requires admin privileges.
    security:
      - bearerAuth: []
    responses:
      '200':
        description: A list of user objects.
      '403':
        description: Forbidden. User is not an admin.
    """
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

@admin_bp.route('/users/<int:user_id>', methods=['PATCH'])
@jwt_required()
@admin_required
def update_user_approval(user_id):
    """
    Update a user's approval status
    ---
    tags:
      - Admin
    summary: Update a user's approval status (Admin Only)
    description: Allows an admin to approve or deactivate a user account, typically for verifying new farmers.
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: user_id
        required: true
        schema: { type: integer }
        description: The ID of the user to update.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [is_approved]
            properties:
              is_approved:
                type: boolean
                example: true
    responses:
      '200':
        description: User updated successfully.
      '403':
        description: Forbidden. User is not an admin.
      '404':
        description: Not Found. No user with the given ID was found.
    """
    user = db.get_or_404(User, user_id)
    json_data = request.get_json()
    try:
        data = user_update_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    user.is_approved = data['is_approved']
    db.session.commit()
    return jsonify(user_schema.dump(user)), 200