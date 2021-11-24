from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dbhost:dbhost-0374@localhost:5432/step_phonebook"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "Zgpou2Q7RIFjNIpRNLz7YpviEFK5gKnC1IlNjo1j7NDrw8zWG4VmWtZrKHJ9F8K"


db = SQLAlchemy(app)

import api.controllers