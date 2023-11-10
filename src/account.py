from app import app, users_db
from flask import request, jsonify
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required, current_user


@app.route("/change_email", methods=["POST"])
@jwt_required()
def change_email():
    if "newEmail" not in request.json:
        return jsonify({"message": "Missing newEmail field", "code": 400})
    
    newEmail = request.json.get("newEmail")

    users_db.update_one(
        {"nickname": current_user["nickname"]}, {"$set": {"email": newEmail}}
    )
    return jsonify({"message": "Success", "code": 200})


@app.route("/change_password", methods=["POST"])
@jwt_required()
def change_password():
    if "newPassword" not in request.json:
        return jsonify({"message": "Missing newPassword field", "code": 400})
    
    newPassword = request.json.get("newPassword")
    if len(newPassword.strip()) == 0:
        return jsonify(
            {"message": "Password has no non-whitespace symbols", "code": 418}
        )

    users_db.update_one(
        {"nickname": current_user["nickname"]},
        {"$set": {"password": newPassword}},
    )
    return jsonify({"message": "Success", "code": 200})

# Define an endpoint for retrieving is user is owner of item
@app.route("/is_owner/<item_id>", methods=["GET"])
@jwt_required()  # Requires a valid JWT token
def is_owner(item_id):
    user = current_user

    if user:
        user_items = user.get("items", [])
        item_id = ObjectId(item_id)

        for item in user_items:
            if item["_id"] == item_id:
                return jsonify({"isOwner": True})

        return jsonify({"isOwner": False})
    else:
        return jsonify({"message": "User not found", "code": 404})
