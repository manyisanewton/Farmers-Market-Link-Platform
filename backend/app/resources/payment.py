# app/resources/payment.py
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User
from app.models.order import Order
from app.models.transaction import Transaction
from app.services import mpesa_service
from app import db

payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route('/initiate/<int:order_id>', methods=['POST'])
@jwt_required()
def initiate_payment(order_id):
    """
    Initiate M-Pesa STK Push for an order
    ---
    tags:
      - Payments
    summary: Initiate payment for a specific order
    description: Allows a logged-in buyer to start the payment process for their own order. Triggers an STK push to the buyer's registered phone number.
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: order_id
        required: true
        schema:
          type: integer
        description: The ID of the order to be paid for.
    responses:
      '200':
        description: STK push initiated successfully.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Payment initiated successfully. Please check your phone.
      '400':
        description: Bad Request. Order is not in a payable state or user has no phone number.
      '403':
        description: Forbidden. The user is not authorized to pay for this order.
      '404':
        description: Not Found. The specified order ID does not exist.
      '500':
        description: Internal Server Error. Failed to communicate with the M-Pesa API.
    """
    buyer_id = int(get_jwt_identity())
    order = db.session.get(Order, order_id)

    if not order:
        return jsonify(message="Order not found."), 404
    if order.buyer_id != buyer_id:
        return jsonify(message="You are not authorized to pay for this order."), 403
    if order.status not in ["Pending", "Pending Payment"]:
         return jsonify(message=f"Order is not in a payable state. Current status: {order.status}"), 400

    buyer = db.session.get(User, buyer_id)
    if not buyer.phone_number:
        return jsonify(message="No phone number on file for this user."), 400

    response = mpesa_service.initiate_stK_push(
        phone_number=buyer.phone_number,
        amount=order.total_price,
        order_id=order.id
    )

    if response and response.get("ResponseCode") == "0":
        new_transaction = Transaction(
            order_id=order.id,
            amount=order.total_price,
            phone_number=buyer.phone_number,
            checkout_request_id=response['CheckoutRequestID']
        )
        order.status = "Pending Payment"
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify(message="Payment initiated successfully. Please check your phone."), 200
    
    return jsonify(message="Failed to initiate payment.", details=response), 500

@payment_bp.route('/callback', methods=['POST'])
def payment_callback():
    """
    M-Pesa Payment Callback URL
    ---
    tags:
      - Payments
    summary: M-Pesa Payment Callback
    description: >
      A public webhook for the Safaricom Daraja API to post the results of an STK push transaction.
      **This endpoint should not be called directly by frontend clients.**
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            description: The payload structure sent by the Safaricom API.
            example:
              Body:
                stkCallback:
                  MerchantRequestID: "29115-34620561-1"
                  CheckoutRequestID: "ws_CO_191220191020363925"
                  ResultCode: 0
                  ResultDesc: "The service request is processed successfully."
                  CallbackMetadata:
                    Item:
                      - { Name: "Amount", Value: 1.00 }
                      - { Name: "MpesaReceiptNumber", Value: "NLJ11HAY6Q" }
                      - { Name: "TransactionDate", Value: 20191219102115 }
                      - { Name: "PhoneNumber", Value: 254712345678 }
    responses:
      '200':
        description: Callback processed successfully.
      '400':
        description: Invalid callback data received.
      '404':
        description: Transaction corresponding to the CheckoutRequestID was not found.
    """
    data = request.get_json()
    
    if not data or "Body" not in data or "stkCallback" not in data["Body"]:
        return jsonify(result="Invalid callback data"), 400

    callback_data = data["Body"]["stkCallback"]
    checkout_request_id = callback_data["CheckoutRequestID"]
    result_code = callback_data["ResultCode"]
    transaction = Transaction.query.filter_by(checkout_request_id=checkout_request_id).first()

    if not transaction:
        print(f"Transaction not found for CheckoutRequestID: {checkout_request_id}")
        return jsonify(result="Transaction not found"), 404

    if result_code == 0:
        metadata = {item["Name"]: item.get("Value") for item in callback_data["CallbackMetadata"]["Item"]}
        transaction.mpesa_receipt_number = metadata.get("MpesaReceiptNumber")
        transaction.status = "Success"
        order = transaction.order
        order.status = "Confirmed"
    else:
        transaction.status = "Failed"
        order = transaction.order
        order.status = "Pending"

    db.session.commit()
    return jsonify(result="Callback processed successfully"), 200