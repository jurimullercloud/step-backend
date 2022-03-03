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
PG_HOST = os.environ.get("PG_HOST")

HOST = PG_HOST if PG_HOST is not None else "localhost"

DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:5432/{POSTGRES_DB}"


# DB_URL = "postgresql://TESTUSER:TESTPassword@localhost:5432/local_db"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = environ.get("JWT_SECRET_KEY")

app.config["SECRET_KEY"]="DEV KEY"
db = SQLAlchemy(app)

import api.controllers
from api.controllers import tests