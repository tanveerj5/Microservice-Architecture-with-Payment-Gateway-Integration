from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["microservices_db"]  # Database name
users_collection = db["users"]  # Collection name


# Helper function to convert ObjectId to string
def user_json(user):
    user["_id"] = str(user["_id"])  # Convert ObjectId to string from JSON response
    return user


@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user"""
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400  # Bad request

    data = request.get_json()  # Parse JSON data from request body

    if (
        "name" not in data
        or "email" not in data
        or data["name"] == ""
        or data["email"] == ""
    ):
        return jsonify({"message": "Missing name or email"}), 400  # Bad request

    # Check if email already exists
    if users_collection.find_one({"email": data["email"]}) is not None:
        return jsonify({"message": "Email already exists"})

    new_user = {
        "name": data["name"],
        "email": data["email"],
    }

    # Insert user into MongoDB
    user_id = users_collection.insert_one(new_user).inserted_id
    return jsonify({"message": "User created", "id": str(user_id)}), 201


@app.route("/users/<string:user_id>", methods=["GET "])
def get_user(user_id):
    """Get a user by user_id"""
    # Invalid request
    if not ObjectId.is_valid(user_id):
        return jsonify({"message": "Invalid user_id"}), 400

    # Find user by ObjectId in MongoDB
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if user:
        return jsonify(user_json(user))

    return jsonify({"message": "User not found"}), 404


if __name__ == "__main__":
    app.run(port=5001, debug=True)
