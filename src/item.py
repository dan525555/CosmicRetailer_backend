import os
from app import app, fs, users_db, items_db
from utils import convert_to_json_serializable, allowed_file
from flask import request, jsonify
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required, current_user  # Import JWT
import json

# Define an endpoint for retrieving a specific item by item_id
@app.route("/get_item/<item_id>", methods=["GET"])
@jwt_required()  # Requires a valid JWT token
def get_item(item_id):
    item_id = ObjectId(item_id)  # Convert the item_id to ObjectId

    items = items_db.find_one({"_id": item_id})
    if items:
        items_serializable = json.loads(
            json.dumps(items, default=convert_to_json_serializable)
        )

        # find user by id
        user = users_db.find_one({"_id": ObjectId(items_serializable["userId"])})
        if user:
            user_serializable = json.loads(
                json.dumps(user, default=convert_to_json_serializable)
            )

            user_data = {
                "id": user_serializable["_id"],
                "nickname": user_serializable["nickname"],
                "email": user_serializable["email"],
                "address": user_serializable["address"],
            }
            return jsonify({"item": items_serializable, "user": user_data, "message": "Success", "code": 200})

        return jsonify({"message": "User not found", "code": 404})
        
    return jsonify({"message": "Item not found", "code": 404})


# Define an endpoint for adding a new item
@app.route("/add_item", methods=["POST"])
@jwt_required()  # Requires a valid JWT token
def add_item():
    user = current_user

    if user:
        item_data = request.form.to_dict()

        required_fields = ["name", "description", "price", "quantity", "category"]

        if not all(field in item_data for field in required_fields):
            return jsonify(
                {
                    "message": "Missing required fields",
                    "code": 400,
                    "required_fields": required_fields,
                }
            )

        item_data["price"] = float(item_data["price"])
        item_data["quantity"] = int(item_data["quantity"])
        item_data["userId"] = str(user["_id"])

        if "photo" in request.files:
            photo = request.files["photo"]
            if photo and allowed_file(photo.filename):
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))
                item_data["photoUrl"] = f"https://cosmicretailer.onrender.com/static/ing/{photo.filename}"
            item_data["photoUrl"] = None
        else:
            item_data["photoUrl"] = None

        item_id = ObjectId()
        item_data["_id"] = item_id

        user_items = user.get("items", [])
        user_items.append(item_data)

        items_db.insert_one(item_data)

        # Update the user's items in the database
        users_db.update_one(
            {"_id": user["_id"]}, {"$set": {"items": user_items}}
        )
        return jsonify({"id": str(item_id), "message": "Item added successfully", "code": 200})
    else:
        return jsonify({"message": "User not found", "code": 404})


# Define an endpoint for deleting an item
@app.route("/delete_item/<item_id>", methods=["DELETE"])
@jwt_required()  # Requires a valid JWT token
def delete_item(item_id):
    user = current_user

    if user:
        user_items = user.get("items", [])
        item_id = ObjectId(item_id)

        if item_id in [item.get("_id") for item in user_items]:
            user_items = [
                item for item in user_items if item.get("_id") != item_id
            ]

            # Update the user's items in the database
            users_db.update_one(
                {"_id": user["_id"]}, {"$set": {"items": user_items}}
            )

            # Delete the item from the items database
            items_db.delete_one({"_id": item_id})

            return jsonify(
                {"message": "Item deleted successfully", "code": 200}
            )
        else:
            return jsonify({"message": "Item not found", "code": 404})
    else:
        return jsonify({"message": "User not found", "code": 404})


# Define an endpoint for updating an item
@app.route("/update_item/<item_id>", methods=["PUT"])
@jwt_required()  # Requires a valid JWT token
def update_item(item_id):
    user = current_user

    if user:
        user_items = user.get("items", [])
        item_id = ObjectId(item_id)

        # Find the index of the item to update
        item_index = None
        for i, item in enumerate(user_items):
            if item.get("_id") == item_id:
                item_index = i
                break

        if item_index is not None:
            new_item_data = request.form.to_dict()
            user_items[item_index].update(new_item_data)

            # Update the user's items in the database
            users_db.update_one(
                {"_id": user["_id"]}, {"$set": {"items": user_items}}
            )

            # Update the item in the items database
            items_db.update_one({"_id": item_id}, {"$set": new_item_data})
            return jsonify(
                {"message": "Item updated successfully", "code": 200}
            )
        else:
            return jsonify({"message": "Item not found", "code": 404})
    else:
        return jsonify({"message": "User not found", "code": 404})
