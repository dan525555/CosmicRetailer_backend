from app import app, users_db
from flask import request, jsonify
from bson.objectid import ObjectId
from flask_jwt import jwt_required, current_identity  # Import JWT

# Define an endpoint for displaying a specific user's items
@app.route("/user_items/<user_id>", methods=["GET"])
def get_specific_user_items(user_id):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    start = (page - 1) * per_page
    end = start + per_page

    user = users_db.find_one({"_id": ObjectId(user_id)})

    if user:
        user_items = user.get('items', [])
        return jsonify({"items": user_items[start:end], "message": "Success", "code": 200})
    else:
        return jsonify({"message": "User not found", "code": 404})

# Define an endpoint to retrieve all items for all users
@app.route("/all_items", methods=["GET"])
@jwt_required()
def get_all_items():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    start = (page - 1) * per_page
    end = start + per_page  

    all_items = []

    for user in users_db.find():
        user_items = user.get('items', [])
        all_items.extend(user_items)

    paginated_items = all_items[start:end]

    return jsonify({"items": paginated_items, "message": "Success", "code": 200})