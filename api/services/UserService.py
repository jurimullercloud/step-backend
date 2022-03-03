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
    

    def get_by_filter(self, first = False, **kwargs):
        res = self._user.query.filter_by(**kwargs) 
        return res if not first else res.first()

    def get_by_id(self, _id: any) -> User:
        return self.get_by_filter(first=True, id=_id)

    def get_all(self) -> List[User]:
        return self._user.query.all()

    def update(self, user: User, schema: Dict) -> User:
        if schema["username"]:
            user.username = schema["username"]
        if schema["password"]:
            _hash = generate_password_hash(schema["password"])
            user.password = _hash

        self._session.commit()
        return user

    def delete(self, user: User) -> int:
        self._session.delete(user) 
        self._session.commit()


userService = UserService(db.session, User)