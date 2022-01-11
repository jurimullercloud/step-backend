from typing import List, Dict
from api import db
from api.data.entities import User
from api.data.schemas import UserSchema, AuthUserSchema, UpdateUserSchema
from api.utils.auth import generate_password_hash

class UserService:

    def __init__(self, session: None, user: User) -> None: 
        self._session = session
        self._user = user
    
    def create(self, user: User) -> User:
        self._session.add(user)
        self._session.commit()

        return user
    
    def get_by_id(self, _id: any) -> User:
        return self._user.query.filter_by(id=_id).first()

    def get_all(self) -> List[User]:
        return self._user.query.all()

    def update(self, schema: Dict) -> User:
        if schema["username"]:
            self._user.username = schema["username"]
        if schema["password"]:
            hash = generate_password_hash(schema["password"])
            self._user.password = hash 

        self._session.commit()
        return self._user

    def delete(self, user: User) -> int:
        self._session.delete(user) 
        self._session.commit()


userService = UserService(db.session, User)