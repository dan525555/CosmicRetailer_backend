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
