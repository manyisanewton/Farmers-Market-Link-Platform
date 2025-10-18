# app/utils/decorators.py
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.models.user import User
from app import db # Import db

def farmer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if user and user.role == 'farmer' and user.is_approved:
            return fn(*args, **kwargs)
        elif user and user.role == 'farmer' and not user.is_approved:
            return jsonify(message="Your farmer account is pending approval."), 403
        else:
            return jsonify(message="Approved farmers access required"), 403
    return wrapper

def buyer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if user and user.role == 'buyer':
            return fn(*args, **kwargs)
        else:
            return jsonify(message="Buyers access required"), 403
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if user and user.role == 'admin':
            return fn(*args, **kwargs)
        else:
            return jsonify(message="Admin access required"), 403
    return wrapper