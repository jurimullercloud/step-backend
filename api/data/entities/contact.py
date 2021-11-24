from sqlalchemy.orm import backref
from api import db

class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.Text, nullable = False, unique = True)
    phone = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"[Id: {self.id}]  UserId: {self.user_id} Name: {self.name} Phone: {self.phone}"
    
    def __init__(self, user_id, name, phone):
        self.user_id = user_id
        self.name    = name
        self.phone   = phone