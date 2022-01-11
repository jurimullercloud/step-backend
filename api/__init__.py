from os import environ
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
cors = CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://dbhost:dbhost-0374@localhost:5432/step_phonebook"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = f"salam"
# app.config["SECRET_KEY"] = "test"

db = SQLAlchemy(app)

import api.controllers
from api.controllers import tests