# backend/app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flasgger import Swagger
import cloudinary

from .config import config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
swagger = Swagger()

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.config['SWAGGER'] = {
        'title': 'FMLP Backend API', 'uiversion': 3,
        'openapi': '3.0.2', 'doc_expansion': 'list',
        'specs_route': '/api/docs/'
    }

    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key=os.environ.get('CLOUDINARY_API_KEY'),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET')
    )
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    swagger.init_app(app)

    # Initialize CORS with robust settings
    CORS(app, resources={r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        "allow_headers": ["Authorization", "Content-Type"]
    }})

    # --- Register Blueprints ---
    from .resources.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # --- THIS IS THE FIX ---
    # The blueprint for /api/users was missing from the last update
    from .resources.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')
    # -----------------------

    from .resources.produce import produce_bp
    app.register_blueprint(produce_bp, url_prefix='/api/produce')

    from .resources.order import order_bp
    app.register_blueprint(order_bp, url_prefix='/api/orders')

    from .resources.payment import payment_bp
    app.register_blueprint(payment_bp, url_prefix='/api/payments')

    from .resources.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    from .resources.market import market_bp
    app.register_blueprint(market_bp, url_prefix='/api/market')

    from .resources.sms import sms_bp
    app.register_blueprint(sms_bp, url_prefix='/api/sms')

    return app