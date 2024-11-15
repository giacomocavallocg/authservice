from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from main.exceptions.api_exceptions import ApiExceptionBuilder
from main.models.user import UserRepository, User

class UserController:


    def __init__(self) -> None:
        self.blueprint = Blueprint('user_controller', __name__, url_prefix="/users")
        self.blueprint.add_url_rule("/", "getAll", self.get_all, methods=["GET"])
        self.blueprint.add_url_rule("/me", "Me", self.get_info, methods=["GET"])

        self.user_repo = UserRepository()

    @jwt_required()
    def get_all(self):
        users =  self.user_repo.get_all()
        return jsonify(
            [__class__._to_dto(user)for user in users]
            )
    
    @jwt_required()
    def get_info(self):
        current_user = get_jwt_identity()
        user =  self.user_repo.get_by_id(current_user)

        if user is None:
            raise ApiExceptionBuilder.user_not_found()
    
        return jsonify(
            __class__._to_dto(user)
        )
    
    @staticmethod
    def _to_dto(user: User):
        return {"id": user.id, "name": user.name, "email": user.email, "name": user.name, "surname":user.surname, "age": user.age}





