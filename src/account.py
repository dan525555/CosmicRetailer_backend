from app import app, users_db
from flask import request, jsonify
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required, current_user


@app.route("/change_email", methods=["POST"])
@jwt_required()
def change_email():
    if "new_email" not in request.json:
        return jsonify({"message": "Missing new_email field", "code": 400})
    
    new_email = request.json.get("new_email")

    users_db.update_one(
        {"nickname": current_user["nickname"]}, {"$set": {"email": new_email}}
    )
    return jsonify({"message": "Success", "code": 200})


@app.route("/change_password", methods=["POST"])
@jwt_required()
def change_password():
    if "new_password" not in request.json:
        return jsonify({"message": "Missing new_password field", "code": 400})
    
    new_password = request.json.get("new_password")
    if len(new_password.strip()) == 0:
        return jsonify(
            {"message": "Password has no non-whitespace symbols", "code": 418}
        )

    users_db.update_one(
        {"nickname": current_user["nickname"]},
        {"$set": {"password": new_password}},
    )
    return jsonify({"message": "Success", "code": 200})
