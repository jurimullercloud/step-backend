from os import environ
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
cors = CORS(app)

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
RUNNING_ENV = os.environ.get("RUNNING_ENV")
DB_SERVICE_NAME = os.environ.get("DB_SERVICE_NAME")

if RUNNING_ENV != "TEST":
    HOST = os.environ.get(f"{DB_SERVICE_NAME.upper()}_SERVICE_HOST") if DB_SERVICE_NAME is not None else "localhost"
    DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:5432/{POSTGRES_DB}"
else:
    DB_URL = "TEST_URL"

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

db = SQLAlchemy(app)

import api.controllers
from api.controllers import tests