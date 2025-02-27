from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

client = MongoClient("mongodb://localhost:27017")
db = client["microservices_db"]
orders_collection = db["payments"]


@app.route("/orders/<string:order_id>/pay", methods=["PUT"])
def update_order_payment_status(order_id):
    """Update order payment status when payment is received"""
    data = request.json
    payment_status = data.get("payment_status", "Pending")

    result = orders_collection.update_one(
        {"order_id": order_id}, {"$set": {"payment_status": payment_status}}
    )

    if result.matched_count:
        return jsonify({"message": "Order updated successfully"})
    return jsonify({"message": "Order not found"}), 404


if __name__ == "__main__":
    app.run(port=5000, debug=True)
