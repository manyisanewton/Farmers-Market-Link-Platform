import json
from tests.test_admin import create_admin_user # Reuse our admin creator
from tests.test_produce import get_auth_token

def test_get_market_prices(test_client, init_database):
    """
    GIVEN market prices exist in the database
    WHEN any logged-in user requests the '/api/market/prices' endpoint
    THEN they should receive a list of all market prices
    """
    # Setup: Admin must create a price first
    admin_token = create_admin_user(test_client)
    headers = {'Authorization': f'Bearer {admin_token}'}
    price_data = {"crop_name": "Maize", "average_price": "35.50", "unit": "kg"}
    test_client.post('/api/market/prices', data=json.dumps(price_data), headers=headers, content_type='application/json')
    
    # Action: A regular user (e.g., a farmer) requests the prices
    farmer_token = get_auth_token(test_client, 'price_checker', 'password123', 'farmer')
    farmer_headers = {'Authorization': f'Bearer {farmer_token}'}
    response = test_client.get('/api/market/prices', headers=farmer_headers)
    
    # Assertion
    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]['crop_name'] == 'Maize'

def test_admin_create_market_price(test_client, init_database):
    """
    GIVEN a logged-in admin
    WHEN they post to the '/api/market/prices' endpoint with valid data
    THEN a new market price should be created
    """
    admin_token = create_admin_user(test_client)
    headers = {'Authorization': f'Bearer {admin_token}'}
    price_data = {"crop_name": "Tomatoes", "average_price": "80.00", "unit": "kg"}
    
    response = test_client.post('/api/market/prices', data=json.dumps(price_data), headers=headers, content_type='application/json')
    
    assert response.status_code == 201
    assert response.get_json()['average_price'] == "80.00"

def test_non_admin_cannot_create_price(test_client, init_database):
    """
    GIVEN a logged-in non-admin user (e.g., a farmer)
    WHEN they attempt to post to the '/api/market/prices' endpoint
    THEN they should receive a 403 Forbidden error
    """
    farmer_token = get_auth_token(test_client, 'naughty_farmer', 'password123', 'farmer')
    headers = {'Authorization': f'Bearer {farmer_token}'}
    price_data = {"crop_name": "Potatoes", "average_price": "50.00", "unit": "kg"}

    response = test_client.post('/api/market/prices', data=json.dumps(price_data), headers=headers, content_type='application/json')
    
    assert response.status_code == 403