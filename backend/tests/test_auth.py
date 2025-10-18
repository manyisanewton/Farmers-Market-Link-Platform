# tests/test_auth.py
import json

def test_register_user(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/api/auth/register' endpoint is posted to (POST)
    THEN a new user should be created, and a 201 status code returned
    """
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "role": "farmer",
        "phone_number": "+254700000001" # <-- FIX: Added phone number
    }
    response = test_client.post('/api/auth/register', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    assert "User created successfully" in response.get_json()['message']

def test_login_user(test_client, init_database):
    """
    GIVEN a registered user
    WHEN the '/api/auth/login' endpoint is posted to (POST) with correct credentials
    THEN access and refresh tokens should be returned with a 200 status code
    """
    # First, register a user to test login
    reg_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "loginpassword",
        "role": "buyer",
        "phone_number": "+254700000002" # <-- FIX: Added phone number
    }
    test_client.post('/api/auth/register', data=json.dumps(reg_data), content_type='application/json')

    # Now, test login
    login_data = {
        "email": "login@example.com",
        "password": "loginpassword"
    }
    response = test_client.post('/api/auth/login', data=json.dumps(login_data), content_type='application/json')
    json_data = response.get_json()

    assert response.status_code == 200
    assert "access_token" in json_data
    assert "refresh_token" in json_data