from flask import Flask
from flask_cors import CORS
import json
import pymongo

app = Flask(__name__)
app.secret_key = "super_secret_key"
CORS(app, supports_credentials=True)
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (("http://localhost:5173", "http://localhost:5000"),)

with open("config.json") as config_file:
    config_data = json.load(config_file)

app.config.update(config_data)

mongo_client = pymongo.MongoClient(app.config["MONGO_API"])
users_db = mongo_client["data"]["users"]
items_db = mongo_client["data"]["items"]

# rationale for that kind of imports:
# https://stackoverflow.com/questions/11994325/how-to-divide-flask-app-into-multiple-py-files
import log_in as log_in
import item as item
import item_lists as item_lists
import favorite as favorite
import bucket as bucket
import user_profile as user_profile
import search as search
import rating as rating
