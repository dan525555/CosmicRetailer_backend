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
        user_items = user.get("items", [])
        item_id = ObjectId(item_id)

        for item in user_items:
            if item["_id"] == item_id:
                # toggle the isFavorite field
                item["isFavorite"] = not item["isFavorite"]
                
                # update the user's items
                users_db.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"items": user_items}},
                )
                return jsonify({"message": "Success", "code": 200})

        return jsonify({"message": "Item not found", "code": 404})
    else:
        return jsonify({"message": "User not found", "code": 404})
