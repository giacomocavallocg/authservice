from main.models.context import db
from typing import List
from main.exceptions.api_exceptions import ApiExceptionBuilder

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=True)
    use_2fv = db.Column(db.Boolean, unique=False, nullable=False)



class UserRepository:
    
    def __init__(self) -> None:
        self.db = db

    def get_all(self) -> List[User]:
        return User.query.all()
    
    
    def get_by_email(self, email:str) -> List[User]:
        return User.query.filter(User.email == email).one_or_none()
    
    def get_by_id(self, id:str) -> List[User]:
        return User.query.filter(User.id == id).one_or_none()
    
    def create_user(self, user: User) -> User:

        if User.query.filter(User.email == user.email).count() > 0:
            raise ApiExceptionBuilder.user_email_alreasy_exists()

        self.db.session.add(user)

        try:
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            print("error")
            raise e