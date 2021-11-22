from app import app
from flask import request
from app.entities import User
from app.entities import Contact


@app.route("/api/v1/contacts/<int:user_id>", methods = ["GET"])
def get_contacts(user_id):
    pass

@app.route("/api/v1/contacts/<int:user_id>/<int:contact_id>", methods = ["GET"])
def get_contact(user_id, contact_id):
    pass

@app.route("/api/v1/contacts/<int:user_id>", methods = ["POST"])
def create_contact(user_id):
    pass

@app.route("/api/v1/contacts/<int:user_id>/<int:contact_id>", method = ["PUT"])
def update_contact(user_id, contact_id):
    pass


@app.route("/api/v1/contacts/<int:user_id>", method = ["DELETE"])
def delete_all_contacts_of_user(user_id):
    pass

@app.route("/api/v1/contacts/<int:user_id>/<int:contact_id>", method = ["DELETE"])
def delete_user(user_id, contact_id):
    pass

@app.route("/api/v1/contacts/delete-users/<int:user_id>", method = ["POST"])
def delete_multiple_users(user_id):
    pass

