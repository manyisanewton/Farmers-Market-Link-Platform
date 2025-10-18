# app/services/twilio_service.py
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from twilio.twiml.messaging_response import MessagingResponse

def send_sms(to_number, message_body):
    """Sends an SMS using Twilio."""
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_number = os.environ.get('TWILIO_PHONE_NUMBER')
    if not all([account_sid, auth_token, twilio_number]):
        print("Twilio credentials not configured. Skipping SMS.")
        return False
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(body=message_body, from_=twilio_number, to=to_number)
        print(f"SMS sent successfully to {to_number}. SID: {message.sid}")
        return True
    except TwilioRestException as e:
        print(f"Error sending SMS to {to_number}: {e}")
        return False

def process_inbound_sms(from_number, message_body):
    """
    Parses the inbound SMS message and returns the appropriate TwiML response.
    """
    from app.models.user import User
    from app.models.market_price import MarketPrice
    from app import db
    
    response = MessagingResponse()
    parts = message_body.strip().upper().split()
    command = parts[0] if parts else ""
    
    if command == "REGISTER" and len(parts) >= 4 and parts[1] == "FARMER":
        try:
            info_str = " ".join(parts[2:])
            name, location = [x.strip() for x in info_str.split(',')]
            
            existing_user = User.query.filter_by(phone_number=from_number).first()
            if existing_user:
                response.message(f"Hello {existing_user.username}! You are already registered with FMLP.")
            else:
                # --- THIS IS THE FIX ---
                # Generate a unique, placeholder email from the phone number
                sanitized_phone = from_number.replace('+', '')
                placeholder_email = f"{sanitized_phone}@fmlp_offline.com"
                
                # Check if this placeholder email somehow already exists
                if User.query.filter_by(email=placeholder_email).first():
                    response.message("An error occurred. Please contact support.")
                    return str(response)
                # -----------------------
                
                password = "password"
                new_farmer = User(
                    username=name.title(),
                    email=placeholder_email, # Use the placeholder email
                    phone_number=from_number,
                    role='farmer',
                    is_approved=False
                )
                new_farmer.set_password(password)
                db.session.add(new_farmer)
                db.session.commit()
                response.message(f"Welcome, {name.title()}! Your FMLP account has been created and is pending approval. We will notify you once it's active.")
        except Exception as e:
            response.message("Sorry, there was an error processing your registration. Please use the format: REGISTER FARMER Your Name, Your Location")
            print(f"SMS Registration Error: {e}")

    elif command == "PRICE" and len(parts) == 2:
        crop_name = parts[1].capitalize()
        price_entry = MarketPrice.query.filter_by(crop_name=crop_name).first()
        if price_entry:
            msg = f"Current market price for {price_entry.crop_name}: {price_entry.average_price} KES/{price_entry.unit}"
            response.message(msg)
        else:
            response.message(f"Sorry, we do not have a market price for '{crop_name}'.")

    else:
        help_text = (
            "Sorry, I did not understand that command. Available commands:\n"
            "- REGISTER FARMER Your Name, Your Location\n"
            "- PRICE [CropName] (e.g., PRICE MAIZE)"
        )
        response.message(help_text)
        
    return str(response)