# backend/create_admin.py
import os
from getpass import getpass
from app import create_app, db
from app.models.user import User

# Create a minimal app instance to work with the database
config_name = os.getenv('FLASK_ENV', 'default')
app = create_app(config_name)

# Push an application context to make the db connection available
with app.app_context():
    print("--- Create FMLP Admin User ---")
    
    email = input("Enter admin email: ")
    if User.query.filter_by(email=email).first():
        print(f"Error: User with email {email} already exists.")
        exit()
        
    username = input("Enter admin username: ")
    if User.query.filter_by(username=username).first():
        print(f"Error: User with username {username} already exists.")
        exit()

    password = getpass("Enter admin password: ")
    confirm_password = getpass("Confirm admin password: ")
    if password != confirm_password:
        print("Error: Passwords do not match.")
        exit()
        
    phone_number = input("Enter admin phone number (e.g., +2547...): ")
    if User.query.filter_by(phone_number=phone_number).first():
        print(f"Error: User with phone number {phone_number} already exists.")
        exit()
        
    admin_user = User(
        username=username,
        email=email,
        phone_number=phone_number,
        role='admin',
        is_approved=True
    )
    admin_user.set_password(password)
    
    db.session.add(admin_user)
    db.session.commit()
    
    print(f"\nAdmin user '{username}' created successfully!")