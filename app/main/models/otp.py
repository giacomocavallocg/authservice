from main.models.context import db

class UserOtp(db.Model):
    __tablename__ = 'userotps'
    request_id = db.Column(db.String(80), primary_key=True)
    otp = db.Column(db.String(80), nullable=False)
    expiration_date = db.Column(db.DateTime(timezone=True), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class UserOtpRepository:
    
    def __init__(self) -> None:
        self.db = db
    
    def get(self, request_id:str) -> UserOtp:
        return UserOtp.query.filter(UserOtp.request_id == request_id).one_or_none()
    
    def create_otp(self, user_otp: UserOtp) -> UserOtp:

        self.db.session.add(user_otp)

        try:
            db.session.commit()
            return user_otp
        except Exception as e:
            db.session.rollback()
            raise e