from flask_bcrypt import Bcrypt

class PasswordHasher:

    def __init__(self) -> None:
        self.bcrypt = Bcrypt()
    
    def hash_password(self, password:str) -> str:
        return self.bcrypt.generate_password_hash(password).decode('utf-8') 

    def is_valid(self, hashed_password, password):
        return self.bcrypt.check_password_hash(hashed_password, password) 