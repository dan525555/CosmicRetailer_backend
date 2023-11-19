from app import app, fs, users_db, items_db
from flask import jsonify, request
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required, current_user  # Import JWT
import requests
from utils import serialize_object_ids

# Define an endpoint for toggle bucket item by item_id
@app.route("/toggle_bucket/<item_id>", methods=["PUT"])
@jwt_required()  # Requires a valid JWT token
def toggle_bucket(item_id):
    user = current_user

    if user:
        headers = {"Authorization": f"{request.headers.get('Authorization')}"}

        # Check if the current user is the owner of the item
        is_owner_response = requests.get(f"https://cosmicretailer.onrender.com/is_owner/{item_id}", headers=headers)
        is_owner_data = is_owner_response.json()

        if is_owner_data['isOwner']:
            return jsonify({"message": "You can't favorite your own item", "code": 400})
        
        bucket_items = user.get("buckets", [])

        for item in bucket_items:
            if item["_id"] == item_id:
                bucket_items.remove(item)
                users_db.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"buckets": bucket_items}},
                )
                return jsonify({"message": "Success", "code": 200})
        
        bucket_items.append({"_id": item_id})
        users_db.update_one(
            {"_id": user["_id"]},
            {"$set": {"buckets": bucket_items}},
        )

        return jsonify({"message": "Success", "code": 200})
    else:
        return jsonify({"message": "User not found", "code": 404})
    
# Define an endpoint for checking if an item is bucket
@app.route("/is_in_bucket/<item_id>", methods=["GET"])
@jwt_required()  # Requires a valid JWT token
def is_bucket(item_id):
    user = current_user

    if user:
        bucket_items = user.get("buckets", [])

        for item in bucket_items:
            if item["_id"] == item_id:
                return jsonify({"isBucket": True})

        return jsonify({"isBucket": False})
    else:
        return jsonify({"message": "User not found", "code": 404})
    
# Define an endpoint for retrieving all bucket items
@app.route("/get_bucket", methods=["GET"])
@jwt_required()  # Requires a valid JWT token
def get_bucket():
    user = current_user

    if user:
        bucket_items = user.get("buckets", [])
        bucket_items_copy = bucket_items.deepcopy()
        bucket = []

        for item in bucket_items:
            item_id = item["_id"]
            item = items_db.find_one({"_id": item_id})
            if item:
                item["_id"] = str(item["_id"])
                bucket.append(item)
            else:
                bucket_items.remove(item)
                users_db.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"buckets": bucket_items}},
                )

        return jsonify({"bucketItems": serialize_object_ids(bucket), "message": "Success", "code": 200})
    else:
        return jsonify({"message": "User not found", "code": 404})