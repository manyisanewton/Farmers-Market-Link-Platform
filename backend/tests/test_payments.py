# tests/test_payments.py
import json
from unittest.mock import patch

from tests.test_produce import get_auth_token, create_produce_helper, register_user_helper

def create_test_order(test_client, buyer_token, produce_id):
    """Helper to create an order and return its ID."""
    order_data = {"items": [{"produce_id": produce_id, "quantity": 1}]}
    headers = {'Authorization': f'Bearer {buyer_token}'}
    response = test_client.post('/api/orders/', data=json.dumps(order_data), headers=headers, content_type='application/json')
    assert response.status_code == 201
    return response.get_json()['id']

@patch('app.resources.payment.mpesa_service.initiate_stk_push') # Patch where it is used
def test_initiate_payment(mock_initiate_stk, test_client, init_database):
    """
    GIVEN a logged-in buyer with an existing order
    WHEN they post to the '/api/payments/initiate/<order_id>' endpoint
    THEN the mpesa_service.initiate_stk_push function should be called
    """
    farmer_token = get_auth_token(test_client, 'paymentfarmer', 'password123', 'farmer')
    buyer_token = get_auth_token(test_client, 'paymentbuyer', 'password123', 'buyer')
    produce_id = create_produce_helper(test_client, farmer_token)
    order_id = create_test_order(test_client, buyer_token, produce_id)

    mock_initiate_stk.return_value = {"ResponseCode": "0", "CheckoutRequestID": "ws_CO_12345"}
    
    headers = {'Authorization': f'Bearer {buyer_token}'}
    response = test_client.post(f'/api/payments/initiate/{order_id}', headers=headers)
    
    assert response.status_code == 200
    assert "Payment initiated successfully" in response.get_json()['message']
    mock_initiate_stk.assert_called_once()

def test_payment_callback_success(test_client, init_database):
    """
    GIVEN an order and transaction exist in a pending state
    WHEN the '/api/payments/callback' endpoint is called by Safaricom with a success payload
    THEN the order and transaction statuses should be updated to 'Success'
    """
    from app.models.user import User
    from app.models.order import Order
    from app.models.transaction import Transaction
    from app import db
    
    # FIX: Register a user and get their actual ID
    buyer_creds = register_user_helper(test_client, 'callback_buyer', 'password123', 'buyer')
    buyer_user = User.query.filter_by(email=buyer_creds['email']).first()
    assert buyer_user is not None
    
    # Use the actual buyer_id from the database
    order = Order(buyer_id=buyer_user.id, total_price=120.00, status="Pending Payment")
    db.session.add(order)
    db.session.commit()
    
    transaction = Transaction(
        order_id=order.id, amount=120.00, 
        phone_number="+254712345678", checkout_request_id="ws_CO_SUCCESS_123"
    )
    db.session.add(transaction)
    db.session.commit()
    
    success_payload = {
        "Body": {
            "stkCallback": {
                "ResultCode": 0,
                "ResultDesc": "The service request is processed successfully.",
                "CheckoutRequestID": "ws_CO_SUCCESS_123",
                "CallbackMetadata": {
                    "Item": [
                        {"Name": "Amount", "Value": 120.00},
                        {"Name": "MpesaReceiptNumber", "Value": "QWERTY1234"},
                        {"Name": "PhoneNumber", "Value": 254712345678}
                    ]
                }
            }
        }
    }
    response = test_client.post('/api/payments/callback', data=json.dumps(success_payload), content_type='application/json')
    
    assert response.status_code == 200
    updated_order = db.session.get(Order, order.id)
    assert updated_order.status == "Confirmed"
    updated_transaction = db.session.get(Transaction, transaction.id)
    assert updated_transaction.status == "Success"