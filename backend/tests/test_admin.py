# tests/test_admin.py
import json
from tests.test_produce import login_user_helper, register_user_helper

def create_admin_user(test_client):
    """Helper to create and log in an admin user."""
    from app.models.user import User
    from app import db
    
    # Admins are created programmatically, not via API
    admin_email = "admin@fmlp.com"
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        admin_user = User(
            username='adminuser', email=admin_email,
            role='admin', is_approved=True, phone_number='+254799999999'
        )
        admin_user.set_password('adminpass')
        db.session.add(admin_user)
        db.session.commit()
    
    return login_user_helper(test_client, admin_email, 'adminpass')

def test_admin_get_all_users(test_client, init_database):
    """
    GIVEN a logged-in admin
    WHEN they request the '/api/admin/users' endpoint
    THEN they should receive a list of all users
    """
    admin_token = create_admin_user(test_client)
    # Create another user to ensure the list has multiple entries
    register_user_helper(test_client, 'testfarmer', 'password123', 'farmer')
    
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = test_client.get('/api/admin/users', headers=headers)
    
    assert response.status_code == 200
    # There should be 2 users: the admin and the new farmer
    assert len(response.get_json()) == 2

def test_admin_approve_farmer(test_client, init_database):
    """
    GIVEN a logged-in admin and an unapproved farmer
    WHEN the admin sends a PATCH request to approve the farmer
    THEN the farmer's 'is_approved' status should be True
    """
    admin_token = create_admin_user(test_client)
    
    # --- THIS IS THE FIX ---
    # Create an unapproved farmer by explicitly setting is_approved=False
    farmer_creds = register_user_helper(
        test_client, 'unapproved_farmer', 'password123', 'farmer', is_approved=False
    )
    farmer = farmer_creds['user_obj']
    # This assertion will now pass
    assert farmer.is_approved is False

    # Admin approves the farmer
    headers = {'Authorization': f'Bearer {admin_token}'}
    update_data = {"is_approved": True}
    response = test_client.patch(f'/api/admin/users/{farmer.id}', data=json.dumps(update_data), headers=headers, content_type='application/json')
    
    assert response.status_code == 200
    assert response.get_json()['is_approved'] is True