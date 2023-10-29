from app import app, users_db
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from bson import ObjectId


def get_paginated_items(item_list, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    return item_list[start:end]


# Define an endpoint for displaying a specific user's items
@app.route("/user_items/<user_id>", methods=["GET"])
@jwt_required()
def get_specific_user_items(user_id):
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    user = users_db.find_one({"_id": ObjectId(user_id)})

    if user:
        user_items = user.get("items", [])
        paginated_items = get_paginated_items(user_items, page, per_page)
        return jsonify(
            {"items": paginated_items, "message": "Success", "code": 200}
        )
    else:
        return jsonify({"message": "User not found", "code": 404})


# Define an endpoint to retrieve all items for all users
@app.route("/all_items", methods=["GET"])
@jwt_required()
def get_all_items():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    all_items = []

    for user in users_db.find():
        user_items = user.get("items", [])
        all_items.extend(user_items)

    paginated_items = get_paginated_items(all_items, page, per_page)

    return jsonify(
        {"items": paginated_items, "message": "Success", "code": 200}
    )
