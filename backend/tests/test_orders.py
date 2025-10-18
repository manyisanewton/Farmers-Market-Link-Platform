# tests/test_orders.py
import json
from unittest.mock import patch

# FIX: 'setup_produce' is a local function and should NOT be imported.
from tests.test_produce import register_user_helper, login_user_helper, get_auth_token

def setup_produce(test_client, farmer_token):
    """Helper function to create a produce item and return its ID."""
    headers = {'Authorization': f'Bearer {farmer_token}'}
    produce_data = {
        "name": "Test Apples", "price": "120.00",
        "quantity": "50", "unit": "kg"
    }
    response = test_client.post(
        '/api/produce/',
        data=produce_data,
        headers=headers,
        content_type='multipart/form-data'
    )
    assert response.status_code == 201
    return response.get_json()['id']

def test_create_order(test_client, init_database):
    """
    GIVEN a logged-in buyer and an available produce item
    WHEN the '/api/orders/' endpoint is posted to with a valid order
    THEN a new order should be created, and a 201 status code returned
    """
    farmer_token = get_auth_token(test_client, 'orderfarmer', 'password123', 'farmer')
    buyer_token = get_auth_token(test_client, 'orderbuyer', 'password123', 'buyer')
    produce_id = setup_produce(test_client, farmer_token)
    order_data = {"items": [{"produce_id": produce_id, "quantity": 5}]}
    headers = {'Authorization': f'Bearer {buyer_token}'}
    response = test_client.post('/api/orders/', data=json.dumps(order_data), headers=headers, content_type='application/json')
    assert response.status_code == 201
    assert response.get_json()['status'] == 'Pending'

def test_create_order_insufficient_stock(test_client, init_database):
    """
    GIVEN a logged-in buyer
    WHEN they try to order more produce than is available
    THEN the request should fail with a 400 status code
    """
    farmer_token = get_auth_token(test_client, 'stockfarmer', 'password123', 'farmer')
    buyer_token = get_auth_token(test_client, 'stockbuyer', 'password123', 'buyer')
    produce_id = setup_produce(test_client, farmer_token)
    order_data = {"items": [{"produce_id": produce_id, "quantity": 100}]}
    headers = {'Authorization': f'Bearer {buyer_token}'}
    response = test_client.post('/api/orders/', data=json.dumps(order_data), headers=headers, content_type='application/json')
    assert response.status_code == 400
    assert "Insufficient stock" in response.get_json()['message']

def test_get_buyer_orders(test_client, init_database):
    """
    GIVEN a buyer who has placed an order
    WHEN they request the '/api/orders/' endpoint (GET)
    THEN they should see a list of their orders with a 200 status code
    """
    farmer_token = get_auth_token(test_client, 'farmerget', 'password123', 'farmer')
    buyer_token = get_auth_token(test_client, 'buyerget', 'password123', 'buyer')
    produce_id = setup_produce(test_client, farmer_token)
    order_data = {"items": [{"produce_id": produce_id, "quantity": 2}]}
    headers = {'Authorization': f'Bearer {buyer_token}'}
    create_response = test_client.post('/api/orders/', data=json.dumps(order_data), headers=headers, content_type='application/json')
    assert create_response.status_code == 201
    response = test_client.get('/api/orders/', headers=headers)
    assert response.status_code == 200
    assert len(response.get_json()) == 1

@patch('app.resources.order.send_sms') # Patch where the function is used
def test_create_order_sends_sms_notification(mock_send_sms, test_client, init_database):
    """
    GIVEN a new order is created
    WHEN the order is successfully placed
    THEN the Twilio send_sms mock should be called
    """
    # Tell the mock to return True and NOT execute the real code
    mock_send_sms.return_value = True

    farmer_creds = register_user_helper(test_client, 'smsfarmer', 'password123', 'farmer')
    buyer_creds = register_user_helper(test_client, 'smsbuyer', 'password123', 'buyer')
    farmer_token = login_user_helper(test_client, farmer_creds['email'], farmer_creds['password'])
    buyer_token = login_user_helper(test_client, buyer_creds['email'], buyer_creds['password'])
    produce_id = setup_produce(test_client, farmer_token)
    
    order_data = {"items": [{"produce_id": produce_id, "quantity": 1}]}
    headers = {'Authorization': f'Bearer {buyer_token}'}
    response = test_client.post('/api/orders/', data=json.dumps(order_data), headers=headers, content_type='application/json')
    
    assert response.status_code == 201
    mock_send_sms.assert_called_once()

def test_get_farmer_orders(test_client, init_database):
    """
    GIVEN a farmer with produce that has been ordered
    WHEN they request the '/api/orders/farmer' endpoint (GET)
    THEN they should see a list of orders containing their produce
    """
    farmer_token = get_auth_token(test_client, 'farmerview', 'password123', 'farmer')
    buyer_token = get_auth_token(test_client, 'buyerview', 'password123', 'buyer')
    produce_id = setup_produce(test_client, farmer_token)
    order_data = {"items": [{"produce_id": produce_id, "quantity": 2}]}
    create_response = test_client.post('/api/orders/', data=json.dumps(order_data), headers={'Authorization': f'Bearer {buyer_token}'}, content_type='application/json')
    assert create_response.status_code == 201
    farmer_headers = {'Authorization': f'Bearer {farmer_token}'}
    response = test_client.get('/api/orders/farmer', headers=farmer_headers)
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_farmer_update_order_status(test_client, init_database):
    """
    GIVEN a farmer with an active order
    WHEN they send a PATCH request to update the order's status
    THEN the status should be updated, and a 200 status code returned
    """
    farmer_token = get_auth_token(test_client, 'farmerupdate', 'password123', 'farmer')
    buyer_token = get_auth_token(test_client, 'buyerupdate', 'password123', 'buyer')
    produce_id = setup_produce(test_client, farmer_token)
    order_data = {"items": [{"produce_id": produce_id, "quantity": 2}]}
    create_res = test_client.post('/api/orders/', data=json.dumps(order_data), headers={'Authorization': f'Bearer {buyer_token}'}, content_type='application/json')
    order_id = create_res.get_json()['id']
    update_data = {"status": "Confirmed"}
    farmer_headers = {'Authorization': f'Bearer {farmer_token}'}
    response = test_client.patch(f'/api/orders/{order_id}', data=json.dumps(update_data), headers=farmer_headers, content_type='application/json')
    assert response.status_code == 200
    assert response.get_json()['status'] == "Confirmed"