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
DB_SERVICE_IP = os.environ.get("DB_SERVICE_IP")

if RUNNING_ENV != "TEST":
    DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_SERVICE_IP}:5432/{POSTGRES_DB}"
else:
    DB_URL = "TEST_URL"

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

if RUNNING_ENV == "BACKEND" or RUNNING_ENV == "TEST":
    db = SQLAlchemy(app)
    import api.controllers
    from api.controllers import tests