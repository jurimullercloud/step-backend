from typing import Dict
from api.data.entities import User, Contact
from api.data.schemas import UpdateUserSchema
from api.utils.auth import generate_password_hash



def process_user_update(user_schema: Dict, user: User) -> User:
    if user_schema["username"]:
        user.username = user_schema["username"]
    if user_schema["password"]:
        hash = generate_password_hash(user_schema["password"])
        user.password = hash
    return user

def process_contact_update(contact_schema: Dict, contact: Contact) -> Contact:
    if contact_schema["name"]:
        contact.name = contact_schema["name"]
    if contact_schema["phone"]:
        contact.phone = contact_schema["phone"]
    
    return contact