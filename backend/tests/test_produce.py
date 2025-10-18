# tests/test_produce.py
import json
from app.models.user import User
from app import db

_user_counter = 0

def register_user_helper(test_client, email_prefix, password, role='farmer', phone_number=None, is_approved=True):
    global _user_counter
    _user_counter += 1
    unique_id = f"{email_prefix}{_user_counter}"
    unique_email = f"{unique_id}@example.com"
    final_phone_number = phone_number or f"+254700000{_user_counter:04d}"
    new_user = User(username=unique_id, email=unique_email, role=role, phone_number=final_phone_number, is_approved=is_approved)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return {"email": unique_email, "password": password, "user_obj": new_user}

def login_user_helper(test_client, email, password):
    response = test_client.post('/api/auth/login', data=json.dumps({"email": email, "password": password}), content_type='application/json')
    json_response = response.get_json()
    if 'access_token' not in json_response:
        raise ValueError(f"Failed to log in as {email}. Response: {json_response}")
    return json_response['access_token']

def get_auth_token(test_client, email_prefix, password, role='farmer', is_approved=True):
    user_creds = register_user_helper(test_client, email_prefix, password, role, is_approved=is_approved)
    return login_user_helper(test_client, user_creds['email'], user_creds['password'])

def create_produce_helper(test_client, farmer_token, produce_data=None):
    """Helper function to create a produce item via the API and return its ID."""
    headers = {'Authorization': f'Bearer {farmer_token}'}
    if produce_data is None:
        produce_data = {"name": "Test Apples", "price": "120.00", "quantity": "50", "unit": "kg", "location": "Default"}
    
    # FIX: Send as multipart/form-data, not JSON
    response = test_client.post(
        '/api/produce/',
        data=produce_data,
        headers=headers,
        content_type='multipart/form-data'
    )
    assert response.status_code == 201, f"Failed to create produce. Status: {response.status_code}, Response: {response.get_json()}"
    return response.get_json()['id']

# --- All test functions below this line remain the same, but will now work ---
def test_create_produce_listing(test_client, init_database):
    token = get_auth_token(test_client, 'farmer', 'password123')
    produce_data = {"name": "Fresh Tomatoes", "description": "Locally grown.", "price": "80.50", "quantity": "50", "unit": "kg"}
    produce_id = create_produce_helper(test_client, token, produce_data)
    assert isinstance(produce_id, int)

def test_create_produce_by_buyer_fails(test_client, init_database):
    token = get_auth_token(test_client, 'buyer', 'password123', role='buyer')
    headers = {'Authorization': f'Bearer {token}'}
    produce_data = {"name": "Test Produce", "price": "10.00", "quantity": "5", "unit": "kg"}
    response = test_client.post('/api/produce/', data=produce_data, content_type='multipart/form-data', headers=headers)
    assert response.status_code == 403

def test_get_all_produce(test_client, init_database):
    farmer_token = get_auth_token(test_client, 'farmer', 'password123')
    create_produce_helper(test_client, farmer_token)
    buyer_token = get_auth_token(test_client, 'buyer', 'password123', role='buyer')
    buyer_headers = {'Authorization': f'Bearer {buyer_token}'}
    response = test_client.get('/api/produce/', headers=buyer_headers)
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_update_own_produce_listing(test_client, init_database):
    token = get_auth_token(test_client, 'farmer', 'password123')
    produce_id = create_produce_helper(test_client, token)
    update_data = {"price": "75.00", "quantity": 25}
    headers = {'Authorization': f'Bearer {token}'}
    # Note: PUT requests with JSON are still fine, only the create endpoint changed
    response = test_client.put(f'/api/produce/{produce_id}', data=json.dumps(update_data), headers=headers, content_type='application/json')
    assert response.status_code == 200

def test_filter_produce_by_name(test_client, init_database):
    farmer_token = get_auth_token(test_client, 'filter_farmer', 'password123')
    create_produce_helper(test_client, farmer_token, {"name": "Tomatoes", "price": "80", "quantity": "50", "unit": "kg"})
    create_produce_helper(test_client, farmer_token, {"name": "Potatoes", "price": "60", "quantity": "100", "unit": "kg"})
    buyer_token = get_auth_token(test_client, 'filter_buyer', 'password123', 'buyer')
    headers = {'Authorization': f'Bearer {buyer_token}'}
    response = test_client.get('/api/produce/?name=Tomatoes', headers=headers)
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_filter_produce_by_price_range(test_client, init_database):
    farmer_token = get_auth_token(test_client, 'price_farmer', 'password123')
    create_produce_helper(test_client, farmer_token, {"name": "Item One", "price": "50", "quantity": "10", "unit": "item"})
    create_produce_helper(test_client, farmer_token, {"name": "Item Two", "price": "100", "quantity": "10", "unit": "item"})
    create_produce_helper(test_client, farmer_token, {"name": "Item Three", "price": "150", "quantity": "10", "unit": "item"})
    buyer_token = get_auth_token(test_client, 'price_buyer', 'password123', 'buyer')
    headers = {'Authorization': f'Bearer {buyer_token}'}
    response = test_client.get('/api/produce/?min_price=40&max_price=120', headers=headers)
    assert response.status_code == 200
    assert len(response.get_json()) == 2

def test_filter_produce_by_location(test_client, init_database):
    farmer_token = get_auth_token(test_client, 'location_farmer', 'password123')
    create_produce_helper(test_client, farmer_token, {"name": "Sukuma", "price": "10", "quantity": "1", "unit": "kg", "location": "Eldoret"})
    create_produce_helper(test_client, farmer_token, {"name": "Cabbages", "price": "10", "quantity": "1", "unit": "kg", "location": "Nakuru"})
    create_produce_helper(test_client, farmer_token, {"name": "Onions", "price": "10", "quantity": "1", "unit": "kg", "location": "Eldoret"})
    buyer_token = get_auth_token(test_client, 'location_buyer', 'password123', 'buyer')
    headers = {'Authorization': f'Bearer {buyer_token}'}
    response = test_client.get('/api/produce/?location=Eldoret', headers=headers)
    assert response.status_code == 200
    assert len(response.get_json()) == 2