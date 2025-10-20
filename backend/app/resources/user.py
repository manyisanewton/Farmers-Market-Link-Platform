# backend/app/resources/user.py
from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required
from app.models.user import User
from app.schemas.user import UserSchema
from app import db

user_bp = Blueprint('user_bp', __name__)
user_details_schema = UserSchema(only=("id", "username", "email", "role"))

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_details(user_id):
    """
    Get details for a specific user.
    ---
    tags:
        - Users
    summary: Get user details by ID
    description: Retrieves public details of a user, such as username and role. Requires authentication.
    security:
        - bearerAuth: []
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
    responses:
        '200':
            description: User details retrieved successfully.
        '404':
            description: User not found.
    """
    user = db.get_or_404(User, user_id)
    return jsonify(user_details_schema.dump(user)), 200