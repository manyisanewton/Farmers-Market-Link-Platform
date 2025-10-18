# tests/test_sms.py
import json
from urllib.parse import urlencode

def test_inbound_sms_register_farmer(test_client, init_database):
    """
    GIVEN a new farmer sends a correctly formatted registration SMS
    WHEN Twilio posts to the '/api/sms/inbound' webhook
    THEN a new user should be created, and a success SMS response returned
    """
    # Twilio sends data as a URL-encoded form
    payload = {
        'From': '+254712345678',
        'Body': 'REGISTER FARMER John Doe, Eldoret'
    }
    
    response = test_client.post('/api/sms/inbound', data=urlencode(payload), content_type='application/x-www-form-urlencoded')
    
    assert response.status_code == 200
    # Twilio expects a TwiML response for SMS replies
    assert '<Response>' in response.data.decode()
    assert '<Message>' in response.data.decode()
    assert 'Welcome, John Doe!' in response.data.decode()
    
    # Check that the user was actually created in the DB
    from app.models.user import User
    user = User.query.filter_by(phone_number='+254712345678').first()
    assert user is not None
    assert user.username == 'John Doe'

def test_inbound_sms_get_price(test_client, init_database):
    """
    GIVEN a market price for 'Maize' exists
    WHEN a user texts 'PRICE MAIZE'
    THEN the webhook should return the correct price information
    """
    # Setup: An admin needs to create a market price first
    from app.models.market_price import MarketPrice
    from app import db
    price = MarketPrice(crop_name="Maize", average_price=35.00, unit="kg")
    db.session.add(price)
    db.session.commit()
    
    payload = {
        'From': '+254787654321',
        'Body': 'PRICE MAIZE'
    }
    
    response = test_client.post('/api/sms/inbound', data=urlencode(payload), content_type='application/x-www-form-urlencoded')

    assert response.status_code == 200
    assert 'Current market price for Maize: 35.00 KES/kg' in response.data.decode()

def test_inbound_sms_unknown_command(test_client, init_database):
    """
    GIVEN a user sends an unrecognized command
    WHEN Twilio posts to the webhook
    THEN a help message should be returned
    """
    payload = {
        'From': '+254711111111',
        'Body': 'HELLO WORLD' # An unknown command
    }
    
    response = test_client.post('/api/sms/inbound', data=urlencode(payload), content_type='application/x-www-form-urlencoded')
    
    assert response.status_code == 200
    assert 'Sorry, I did not understand that command.' in response.data.decode()
    assert 'REGISTER FARMER' in response.data.decode() # The help text should contain valid commands