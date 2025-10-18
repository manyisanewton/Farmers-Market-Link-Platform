# app/services/mpesa_service.py
import os
import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime

def get_access_token():
    """Get access token from Safaricom Daraja API."""
    consumer_key = os.environ.get('MPESA_CONSUMER_KEY')
    consumer_secret = os.environ.get('MPESA_CONSUMER_SECRET')
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    try:
        r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        r.raise_for_status()
        return r.json()['access_token']
    except requests.exceptions.RequestException as e:
        print(f"Error getting M-Pesa token: {e}")
        return None

def initiate_stk_push(phone_number, amount, order_id):
    """Initiate an STK Push request to the Safaricom API."""
    access_token = get_access_token()
    if not access_token:
        return None

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Sanitize phone number to 254... format
    if phone_number.startswith('+'):
        phone_number = phone_number[1:]
    if phone_number.startswith('07'):
        phone_number = '254' + phone_number[1:]

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode = os.environ.get('MPESA_SHORTCODE')
    passkey = os.environ.get('MPESA_PASSKEY')
    
    # Create the base64 encoded password
    password_str = shortcode + passkey + timestamp
    password_bytes = password_str.encode('ascii')
    password = base64.b64encode(password_bytes).decode('utf-8')

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount), # Amount must be an integer
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": os.environ.get('MPESA_CALLBACK_URL'),
        "AccountReference": f"FMLP{order_id}",
        "TransactionDesc": f"Payment for Order #{order_id}"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error initiating STK push: {e}")
        return None