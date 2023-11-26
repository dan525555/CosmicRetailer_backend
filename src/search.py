from app import app, items_db
from flask import request, jsonify, send_file
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required, current_user
from utils import serialize_object_ids


@app.route("/find/<text>", methods=["PUT"])
@jwt_required()  # Requires a valid JWT token
def find(text):
    items = items_db.find({"name": "/" + text + "/i" })
    if items:
        return jsonify(
            {"items": serialize_object_ids(items), "message": "Success", "code": 200}
        )
    else:
    	return jsonify({"message": "No items found", "code": 404})