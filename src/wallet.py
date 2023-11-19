from io import BytesIO
from app import app, fs, users_db, items_db, web3
from utils import convert_to_json_serializable
from flask import request, jsonify, send_file
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required, current_user  # Import JWT
import json
import requests

@app.route('/getBalance', methods=['GET'])
@jwt_required()
def getBalance():
    address = current_user['walletAddress']
    account = web3.to_checksum_address(address)
    balance = web3.eth.get_balance(account)

    return json.dumps({'balance': balance})

