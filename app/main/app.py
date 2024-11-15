from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
import logging

from main.models.context import db
from main.services import psw_hasher 
from main.controllers import AuthController, UserController
from main.config import config_by_name
from main.exceptions.api_exceptions import ApiException

def api_exception_handler(e: ApiException):
    return {"code":e.code, "message": e.message}, e.http_code

def exception_handler(e: Exception):
    logging.exception(e)
    return {"code":"500", "message": "internal server error"}, 500

def validation_exception_handler(e: ValidationError):
    return {"code":"400", "message": e.messages}, 400

def create_app(config_name: str="dev"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    jwt = JWTManager(app)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    db.init_app(app)
    with app.app_context():
        db.create_all()

    auth_controller = AuthController()
    user_controller = UserController()

    app.register_blueprint(auth_controller.blueprint)
    app.register_blueprint(user_controller.blueprint)

    app.register_error_handler(ApiException, api_exception_handler)
    app.register_error_handler(ValidationError, validation_exception_handler)

    app.register_error_handler(Exception, exception_handler)

    psw_hasher.bcrypt.init_app(app)

    return app


app = create_app()