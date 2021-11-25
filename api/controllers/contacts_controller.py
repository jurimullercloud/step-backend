from flask import json
from flask.json import jsonify
from api import app, db
from flask import request
from api.controllers.utils import process_contact_update
from api.data.entities import User, Contact
from api.data.schemas.contact import ContactSchema, UpdateContactSchema, DeleteContactSchema
from api.utils.auth import auth_with_jwt
import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/api/v1/users/<int:user_id>/contacts/list", methods=["GET"])
@auth_with_jwt
def get_contacts(user_id):
    contact = Contact.query.filter_by(user_id=id).all()
    if not contact:
        return jsonify({"message": f"Can't find contacts for the user with id {user_id}"})

    return jsonify({"data": ContactSchema(many=True).dump(contact)})


@app.route("/api/v1/users/<int:user_id>/contacts/<int:contact_id>", methods=["GET"])
@auth_with_jwt
def get_contact(user_id, contact_id):
    contact = Contact.query.filter_by(user_id=id, id=contact_id).first()
    if not contact:
        return jsonify({"message": f"Contact not found with the given id {contact_id}"}), 404

    return ContactSchema().dump(contact)


@app.route("/api/v1/users/<int:user_id>/contacts/add", methods=["POST"])
@auth_with_jwt
def create_contact(user_id):
    body = request.get_json()
    if body:
        try:
            # validate user
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return jsonify({"message": "User not found"}), 404

            contact_schema = ContactSchema().load(body)
            contact = Contact(
                user_id, contact_schema["name"], contact_schema["phone"])

            db.session.add(contact)
            db.session.commit()
        except Exception as ex:
            return jsonify({"message": "Server crashed"}), 500
    else:
        return jsonify({"message": "Request body not found"}), 403


@app.route("/api/v1/users/<int:user_id>/contacts/<int:contact_id>/edit", methods=["PUT"])
@auth_with_jwt
def update_contact(user_id, contact_id):
    body = request.get_json()
    if not body:
        return jsonify({"message": "Request body not found"}), 401

    try:
        schema = UpdateContactSchema().load(body)
        contact = Contact.query.filter_by(
            id=contact_id, user_id=user_id).first()

        contact = process_contact_update(schema, contact)
        db.session.commit()

        return ContactSchema().dump(contact)
    except Exception as ex:
        logging.exception(ex)
        return jsonify({"message": "Server crashed"})


@app.route("/api/v1/users/<int:user_id>/contacts/<int:contact_id>/delete", methods=["DELETE"])
@auth_with_jwt
def delete_contact(user_id, contact_id):
    try:
        contact = Contact.query.filter_by(id=contact_id, user_id=user_id).all()
        if not contact:
            return f"Contact with id {contact_id} not found", 

        db.session.delete(contact)
        return jsonify({"message": f"Succesfully deleted contact with id {contact_id}"}), 200
    except Exception as ex:
        logging.exception(ex)
        return jsonify({"message": "Server crashed"}), 500


@ app.route("/api/v1/users/<int:user_id>/contacts/delete", methods = ["POST"])
@ auth_with_jwt
def delete_multiple_contacts(user_id):
    all=request.args.get("all")
    
    try:
        filter_params={"user_id": user_id}
        if (all != True):
            body = request.get_json()
            if not body:
                return jsonify({"message": "Request body not found, to delete all contact pass query param of '?all=True'"}), 403
            schema =  DeleteContactSchema().dump(body)
            filter_params["id"] = schema["user_ids"]
        contacts = Contact.query.filter_by(**filter_params).all()
        
        if not contacts:
            return jsonify({"message": "Requested contacts not found"}), 404
        db.session.delete(contacts)


        return jsonify({"message": f"Successfully deleted all contacts of user {user_id} "}) if all == True else jsonify({"message": f"Successfully deleted contacts of user {user_id}"})
    except Exception as ex:
        logging.exception(ex)
        return jsonify({"message": "Server crashed"})
