from datetime import datetime, timedelta
from app import app, users_db
from flask import request, jsonify
import flask_login as fl
from bson.objectid import ObjectId
from re import fullmatch
from jwt import encode, decode, ExpiredSignatureError
from passlib.hash import pbkdf2_sha256

# login part
login_manager = fl.LoginManager()
login_manager.init_app(app)
logged_users = set()


# user class
class User(fl.UserMixin):
    def __init__(self, name) -> None:
        super().__init__()
        self.id = name


@login_manager.user_loader
def load_user(id):
    id = ObjectId(str(id))
    for user in logged_users:
        if user.id == id:
            return user
    return None


@app.route("/login", methods=["POST"])
def login():
    name = request.form["nickname"]
    password = request.form["password"]
    x = users_db.find_one({"nickname": name})

    if x and pbkdf2_sha256.verify(password, x["password"]):
        user = User(x["_id"])
        fl.login_user(user)

        # Generate a JWT token
        token = encode(
            {"user_id": str(x["_id"])},
            app.secret_key,
            algorithm="HS256",
            datetime=datetime.utcnow() + timedelta(days=1),
        )

        logged_users.add(user)
        return jsonify({"access_token": token, "message": "Success"}), 200

    return jsonify({"message": "Incorrect password or login", "code": 418})


@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    name = request.form["nickname"]
    password = request.form["password"]

    if users_db.find_one({"nickname": name}) is not None:
        return jsonify(
            {"message": "This nickname is already in use", "code": 418}
        )
    if not fullmatch(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email
    ):
        return jsonify(
            {"message": "This is not a proper email address", "code": 418}
        )
    if users_db.find_one({"email": email}) is not None:
        return jsonify({"message": "This email is already in use", "code": 418})

    # Hash the password before storing it
    hashed_password = pbkdf2_sha256.hash(password)

    token = encode(
        {"user_id": str(x["_id"])},
        app.secret_key,
        algorithm="HS256",
        datetime=datetime.utcnow() + timedelta(days=1),
    )

    users_db.insert_one(
        {
            "email": email,
            "nickname": name,
            "password": hashed_password,
            "points": 0,
            "items": [],
            "history": [],
            "address": [],
            "ratings": [],
        }
    )

    x = users_db.find_one({"nickname": name})
    user = User(x["_id"])
    fl.login_user(user)
    return jsonify({"access_token": token, "message": "Success"}), 200


@app.route("/logout", methods=["POST"])
@fl.login_required
def logout():
    logged_users.remove(fl.current_user)
    fl.logout_user()
    return "Success", 200
