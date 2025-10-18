from flask import request, Response, Blueprint
from app.services import twilio_service

sms_bp = Blueprint('sms_bp', __name__)

@sms_bp.route('/inbound', methods=['POST'])
def inbound_sms():
    """
    Public webhook for receiving inbound SMS from Twilio.
    """
    # Twilio sends data as form-encoded, not JSON
    from_number = request.values.get('From', None)
    message_body = request.values.get('Body', '')

    if not from_number:
        return Response("Missing 'From' number.", status=400)

    # Process the logic in the service and get the TwiML response
    twiml_response_str = twilio_service.process_inbound_sms(from_number, message_body)
    
    # Return the response with the correct content type for Twilio
    return Response(twiml_response_str, mimetype='text/xml')