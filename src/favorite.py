from app import app, fs, users_db
from flask import jsonify
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required, current_user  # Import JWT


# Define an endpoint for toggle favorite item by item_id
@app.route("/toggle_favorite/<item_id>", methods=["PUT"])
@jwt_required()  # Requires a valid JWT token
def toggle_favorite(item_id):
    user = current_user

    if user:
        favorite_items = user.get("favorites", [])

        for item in favorite_items:
            if item["_id"] == item_id:
                favorite_items.remove(item)
                users_db.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"favorites": favorite_items}},
                )
                return jsonify({"message": "Success", "code": 200})
        
        favorite_items.append({"_id": item_id})
        users_db.update_one(
            {"_id": user["_id"]},
            {"$set": {"favorites": favorite_items}},
        )

        return jsonify({"message": "Success", "code": 200})
    else:
        return jsonify({"message": "User not found", "code": 404})
    
# Define an endpoint for checking if an item is favorite
@app.route("/is_favorite/<item_id>", methods=["GET"])
@jwt_required()  # Requires a valid JWT token
def is_favorite(item_id):
    user = current_user

    if user:
        favorite_items = user.get("favorites", [])

        for item in favorite_items:
            if item["_id"] == item_id:
                return jsonify({"isFavorite": True})

        return jsonify({"isFavorite": False})
    else:
        return jsonify({"message": "User not found", "code": 404})
