from os import environ
from flask import Flask
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
cors = CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://dbhost:dbhost-0374@${environ['DB_URL']}:5432/step_phonebook"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = f"{environ['JWT_SECRET_KEY']}"

db = SQLAlchemy(app)

import api.controllers