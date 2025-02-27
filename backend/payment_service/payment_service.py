from flask import Flask, request, jsonify
from pymongo import MongoClient
import stripe
from flask_cors import CORS  # Import CORS
import uuid  # For generating unique order IDs

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# OR use more control
# CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

# Configure Stripe API Key (Replace with your actual secret key)
stripe.api_key = "sk_test_MMNDWMvpQe1ES6MzEzMDGu5a00gaF0XBFa"

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017")  # Connect to local MongoDB
db = client["microservices_db"]
payments_collection = db["payments"]
users_collection = db["users"]  # Assuming there's a users collection


@app.route("/pay", methods=["POST"])
def process_payment():
    """Process payment and store transaction in MongoDB"""
    data = request.json
    user_email = data.get("email")  # Get email from request body
    amount = data["amount"]
    currency = data.get("currency", "usd")

    # Automatically generate a predefined test token (Stripe Test Card)
    token = "tok_visa"  # A predefined token for Visa test card. Use any of Stripe's predefined test tokens.

    order_id = str(uuid.uuid4())  # Generate unique order ID

    # Check if user with the provided email exists
    user = users_collection.find_one({"email": user_email})

    if not user:
        return (
            jsonify({"error": "User not found"}),
            404,
        )  # Return error if user doesn't exist

    user_id = str(user["_id"])  # Use user's ObjectId as the user_id

    try:
        # Call Stripe API to create a charge with the predefined token
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            source=token,  # Use the predefined test token
            description=f"Payment for Order {order_id}",
        )

        # Store payment info in MongoDB
        payment_data = {
            "user_id": user_id,
            "order_id": order_id,
            "amount": amount,
            "currency": currency,
            "payment_status": charge["status"],
            "transaction_id": charge["id"],
        }
        payments_collection.insert_one(payment_data)

        return jsonify(
            {
                "message": "Payment Successful",
                "transaction_id": charge["id"],
                "status": charge["status"],
                "order_id": order_id,  # Return the generated order ID
            }
        )

    except stripe.error.CardError as e:
        return jsonify({"error": str(e)}), 400  # Return error if card charge fails


@app.route("/payments/<string:user_id>", methods=["GET"])
def get_payments(user_id):
    """Get all payments made by a specific user"""
    payments = list(payments_collection.find({"user_id": user_id}))

    for payment in payments:
        payment["_id"] = str(payment["_id"])

    return jsonify(payments)


if __name__ == "__main__":
    app.run(port=5002, debug=True)
