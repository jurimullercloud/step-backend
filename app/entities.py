from sqlalchemy.orm import backref
from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(60), nullable = False)
    contacts = db.relationship("Adress", backref="user", lazy = True)

    def __repr__(self):
        return f"[Id {self.id}]: UserName: {self.username} Password: {self.password}"


class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.Text, nullable = False, unique = True)
    phone = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"[Id: {self.id}]  UserId: {self.user_id} Name: {self.name} Phone: {self.phone}"
