from typing import Tuple
import bcrypt
from api import app
import datetime
from functools import wraps
from flask import request, jsonify
import jwt


def auth_with_jwt(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        secret = app.config["SECRET_KEY"]
        header = request.headers.get("Authorization")

        if not header:
            return jsonify({"message": "Authorization header not found"}), 400

        token = header.split(" ")[1]
        try:
            jwt.decode(token, secret, algorithms=["HS256"])
        except Exception as ex:
            print(ex)
            print(ex.__traceback__)
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)         

    return decorated


def generate_jwt(username: str, expiration_delta: datetime.timedelta) -> Tuple[str, any]:
    secret = app.config["SECRET_KEY"]
    expires_on = datetime.datetime.utcnow() + expiration_delta
    encoded_jwt = jwt.encode({"username": username, "exp": expires_on}, \
                                secret, algorithm="HS256")
    
    return encoded_jwt, expires_on

def generate_password_hash(passwd_str: str) -> str:
    passwd_hashed = bcrypt.hashpw(passwd_str.encode("utf-8"), bcrypt.gensalt()) 
    print(len(passwd_hashed))
    return passwd_hashed.decode()

def validate_password_hash(passwd_str: str, hash: str) -> bool:
    return bcrypt.checkpw(passwd_str.encode("utf-8"), hash.encode("utf-8"))