import string
import secrets


otp_alphabet = string.ascii_uppercase + string.digits

OTP_SIZE = 6

class TokenGenerator:

    @staticmethod
    def generate_otp() -> str:
        otp = ''.join(secrets.choice(otp_alphabet) for i in range(OTP_SIZE))
        return otp
