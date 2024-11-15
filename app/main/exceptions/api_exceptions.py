
class ApiException(Exception):

    def __init__(self, code: str, http_code: int, message: str = None) -> None:
        super().__init__(message)
        self.code = code
        self.http_code = http_code
        self.message = message

class ApiExceptionBuilder:

    @staticmethod
    def unauthorize() -> ApiException:
        return ApiException("001", 401, "unauthorize operation")

    @staticmethod
    def invalid_model() -> ApiException:
        return ApiException("002", 400, "Invalid body model")
        
    @staticmethod
    def invalid_password_format() -> ApiException:
        return ApiException("003", 400, "Password must contains a upper case letter, lower case letter, number and simbol")
    
    @staticmethod
    def invalid_email_format() -> ApiException:
        return ApiException("004", 400, "Invalid Email")
    
    @staticmethod
    def user_not_found() -> ApiException:
        return ApiException("005", 404, "User not found")
    
    @staticmethod
    def user_email_alreasy_exists() -> ApiException:
        return ApiException("006", 400, "User already exits")