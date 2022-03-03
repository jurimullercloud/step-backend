from typing import Dict
import datetime
from flask import request, jsonify
from marshmallow.exceptions import ValidationError
from api import app, db
from api.services import userService as service
from api.data.entities import User, Contact
from api.data.schemas.user import UpdateUserSchema, UserSchema, AuthUserSchema
from api.utils.auth import auth_with_jwt, generate_jwt, generate_password_hash, validate_password_hash
from api.controllers.utils import process_user_update
import logging
logging.basicConfig(level=logging.DEBUG)




@app.route("/api/v1/users", methods=["GET"])
@auth_with_jwt
def get_all_users():
    try:
        users = service.get_all()
        schema = UserSchema(many=True)
        return jsonify({"data": schema.dump(users)})
    except Exception as ex:
        logging.exception(ex)
        return jsonify({"message": "Server crashed"}), 500


@app.route("/api/v1/users/<int:user_id>", methods=["GET"])
@auth_with_jwt
def get_user(user_id):
    try:
        user = service.get_by_id(_id = user_id)

        if not user:
            return jsonify({"message": "User not found"}), 404

        schema = UserSchema()
        return jsonify({"message": "Get user successful", "user": schema.dump(user)}), 200
        
    except Exception as ex:
        logging.exception(ex)
        return jsonify({"message": "Server crashed"}), 500


@app.route("/api/v1/users/<int:user_id>", methods=["PUT"])
@auth_with_jwt
def update_user(user_id):
    try:
        user = service.get_by_id(user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404

        body = request.get_json()
        if not body:
            return jsonify({"message": "Found empty request body"}), 400
        schema: Dict = UpdateUserSchema().load(body)
        user = service.update(user, schema)
        print(user.username)
        print(user.id)

        return jsonify({"message": "Update is successful", "user": UserSchema().dump(user)}), 200

    except Exception as ex:
        logging.exception(ex)
        return {"message": "Server crashed"}, 500


@app.route("/api/v1/users/<int:user_id>", methods=["DELETE"])
@auth_with_jwt
def delete_user(user_id):
    try:
        user: User = service.get_by_id(user_id) 

        if not user:
            return {"message": "User not found"}, 403
        # user's all contacts should also be deleted
        contacts = Contact.query.filter_by(user_id=user_id).all()
        if contacts and len(contacts) > 0:
            db.session.delete(contacts)

        service.delete(user)
        return jsonify({"message": f"Successfully deleted user with {user_id}"}), 200

    except Exception as ex:
        logging.exception(ex)
        return jsonify({"message": "Server crashed"}), 500


@app.route("/api/v1/users/auth", methods=["POST"])
def authenticate_user():
    body = request.get_json()
    if body:
        try:
            user_schema: Dict = AuthUserSchema().load(body)
            username = user_schema["username"]
            password = user_schema["password"]

            usr: User = service.get_by_filter(first = True, username=username)

            if not usr:
                return jsonify({"message": "User not found"}), 404

            authenticated = validate_password_hash(password, usr.password)
            if not authenticated:
                return jsonify({"message": "Invalid user credentials"}), 403

            access_token, expiresOn = generate_jwt(
                username, datetime.timedelta(hours=24))
            return jsonify({"accessToken": f"Bearer {access_token}", "expiresOn": str(expiresOn.timestamp()), "user": UserSchema().dump(usr)})

        except Exception as ex:
            logging.error(ex)

            if isinstance(ex, ValidationError):
                return jsonify({"message": ex.messages}), 401
            return jsonify({"message": "Server crashed"}), 500
    else:
        return jsonify({"message": "Request body was not found"}), 406


@app.route("/api/v1/users/register", methods=["POST"])
def register_user():
    # parses body to appropriate Schema
    body = request.get_json()
    if body:
        try:
            user_schema: Dict = AuthUserSchema().load(body)
            username = user_schema["username"]
            password_hash = generate_password_hash(user_schema["password"])

            user = User(username, password_hash)

            user = service.create(user)

            access_token, expiresOn = generate_jwt(
                username, datetime.timedelta(hours=24))
            return jsonify({"accessToken": f"Bearer {access_token}", \
                            "expiresOn": str(expiresOn.timestamp()), \
                            "user": UserSchema().dump(user)})

        except Exception as ex:
            logging.error(ex)
            if isinstance(ex, ValidationError):
                return jsonify({"message": ex.messages}), 401
            else:
                return jsonify({"message": "Server crashed"}), 500

    else:
        return jsonify({"message": "Request body was not found"}), 406
