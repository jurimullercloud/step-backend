from sqlalchemy.orm import backref
from api import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(64), nullable = False)
    contacts = db.relationship("Contact", backref="user", lazy = True)

    def __repr__(self):
        return f"[Id {self.id}]: UserName: {self.username} Password: {self.password}"

    def __init__(self, username, password):
        self.username = username
        self.password = password