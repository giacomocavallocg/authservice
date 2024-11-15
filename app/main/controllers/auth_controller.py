import re
import logging
from flask import Blueprint, request, Request
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta, timezone
from marshmallow import Schema
from main.controllers.dtos import registration_dto_schema, login_dto_schema, twoFactor_schema
from main.models.user import User, UserRepository
from main.models.otp import UserOtp, UserOtpRepository
from main.services import psw_hasher
from main.exceptions.api_exceptions import ApiExceptionBuilder
from main.services.tocken_generator import TokenGenerator
import uuid

class AuthController:

    OTP_DURATION_MINUTES = 5

    def __init__(self) -> None:
        self.blueprint = Blueprint('registration_controller', __name__, url_prefix="/auth")
        self.blueprint.add_url_rule("/registration", "registration", self.registration, methods=["POST"])
        self.blueprint.add_url_rule("/login", "login", self.login, methods=["POST"])
        self.blueprint.add_url_rule("/2fa", "2fa", self.twoFactorAuth, methods=["POST"])
        self.user_repo = UserRepository()
        self.otp_repo = UserOtpRepository()

    
    def registration(self):
        dto = __class__._try_read_body(request, registration_dto_schema)

        if not __class__._validate_password(dto["password"]):
            raise ApiExceptionBuilder.invalid_password_format()

        if not __class__._validate_email(dto["email"]):
                    raise ApiExceptionBuilder.invalid_email_format()

        new_user = User(email = dto["email"], 
                        password_hash = psw_hasher.hash_password(dto["password"]), 
                        name = dto["name"], 
                        surname = dto["surname"], 
                        age = dto["age"], 
                        use_2fv = dto["use_2fv"])
        
        self.user_repo.create_user(new_user)
        return "", 204
        

    def login(self):
        dto = __class__._try_read_body(request, login_dto_schema)

        user: User = self.user_repo.get_by_email(dto["email"])

        if user is None:
            raise ApiExceptionBuilder.unauthorize()

        if not psw_hasher.is_valid(user.password_hash, dto["password"]):
            raise ApiExceptionBuilder.unauthorize()
        
        if user.use_2fv:
            otp = TokenGenerator.generate_otp()
            request_id = str(uuid.uuid4())

            exp_date = datetime.now(timezone.utc) + timedelta(minutes=self.OTP_DURATION_MINUTES) 
            user_otp = UserOtp(user_id=user.id, request_id=request_id, otp=otp, expiration_date=exp_date)
            self.otp_repo.create_otp(user_otp)
            __class__.send_otp(user, otp)

            return {"request_id": request_id, "validation_endpoint":f"{request.host}/auth/2fa"}, 200
        else:
            access_token = create_access_token(identity=user.id)
            return {"token": access_token}, 200

        
    def twoFactorAuth(self):
        dto = __class__._try_read_body(request, twoFactor_schema)

        user_opt = self.otp_repo.get(request_id=dto["request_id"])

        if not __class__._is_otp_valid(user_opt, dto["otp"]):
            raise ApiExceptionBuilder.unauthorize()

        user: User = self.user_repo.get_by_id(user_opt.user_id)

        if not user.use_2fv:
            raise ApiExceptionBuilder.unauthorize()
        
        access_token = create_access_token(identity=user.id)
        return {"token": access_token}, 200


    @staticmethod
    def _try_read_body(request: Request, schema: Schema):
        if not request.is_json:
            raise ApiExceptionBuilder.invalid_model()
        
        body = request.get_json()
        return schema.load(body)

    @staticmethod
    def _is_otp_valid(user_opt:UserOtp, otp:str) -> None:
        if user_opt is None:
            return False
        
        utc_now = datetime.now(timezone.utc)
        utc_exp = user_opt.expiration_date.replace(tzinfo=timezone.utc)
        return user_opt.otp == otp and utc_now <= utc_exp
    
    @staticmethod
    def _validate_password(password: str) -> bool:
        # Regex che verifica:
        # - almeno 8 caratteri
        # - almeno una lettera maiuscola
        # - almeno una lettera minuscola
        # - almeno un numero
        # - almeno un simbolo
        regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
        return bool(re.match(regex, password))
    
    def _validate_email(email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(email_regex, email))
        
    @staticmethod
    def send_otp(user:User, otp:str) -> None:
        logging.info(f"Otp for user {user.email} - {otp}")

