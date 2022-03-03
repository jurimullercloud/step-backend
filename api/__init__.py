from os import environ
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
cors = CORS(app)

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
PG_HOST = os.environ["PG_HOST"]

DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{PG_HOST}:5432/{POSTGRES_DB}"

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = environ.get("JWT_SECRET_KEY")

db = SQLAlchemy(app)

import api.controllers
from api.controllers import tests