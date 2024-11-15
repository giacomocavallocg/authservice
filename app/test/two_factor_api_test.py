from main.models.user import User
from main.models.otp import UserOtp
from main.models.context import db
from main.services import psw_hasher
from datetime import datetime, timezone, timedelta

def test_login_ok(app, client):

    email = "paolo.rossi4@mail.it"
    request_id = "AjiUj-ssd23"
    otp_code = "A1234"
    exp_date = datetime.now(timezone.utc) + timedelta(minutes=5)

    with app.app_context():
        user = User(id=123, email = email,
                    password_hash = "acsdcdsav", 
                    name = "name", 
                    surname = "surname", 
                    age = None, 
                    use_2fv = True)

        otp = UserOtp(user_id=user.id, 
                      request_id=request_id, 
                      otp=otp_code, 
                      expiration_date=exp_date)
        db.session.add(user)
        db.session.add(otp)

        db.session.commit()

    dto = {
        "request_id":request_id,
        "otp": otp_code,
    }
    response = client.post("/auth/2fa", json=dto)
    assert response.status_code == 200
    assert "token" in response.json
    assert response.json["token"] is not None


def test_login_invalid_otp(app, client):

    email = "paolo.rossi5@mail.it"
    request_id = "AjiUj-ssd23"
    otp_code = "A1234"
    exp_date = datetime.now(timezone.utc) + timedelta(minutes=5)

    with app.app_context():
        user = User(id=123, email = email,
                    password_hash = "acsdcdsav", 
                    name = "name", 
                    surname = "surname", 
                    age = None, 
                    use_2fv = True)

        otp = UserOtp(user_id=user.id, 
                      request_id=request_id, 
                      otp=otp_code, 
                      expiration_date=exp_date)
        db.session.add(user)
        db.session.add(otp)

        db.session.commit()

    dto = {
        "request_id":request_id,
        "otp": "INV4L1D",
    }
    response = client.post("/auth/2fa", json=dto)
    assert response.status_code == 401
    assert response.json["code"] is not "001"

def test_login_expired_otp(app, client):

    email = "paolo.rossi6@mail.it"
    request_id = "AjiUj-ssd23"
    otp_code = "A1234"
    exp_date = datetime.now(timezone.utc) + timedelta(minutes=-5)

    with app.app_context():
        user = User(id=123, email = email,
                    password_hash = "acsdcdsav", 
                    name = "name", 
                    surname = "surname", 
                    age = None, 
                    use_2fv = True)

        otp = UserOtp(user_id=user.id, 
                    request_id=request_id, 
                    otp=otp_code, 
                    expiration_date=exp_date)
        db.session.add(user)
        db.session.add(otp)

        db.session.commit()

    dto = {
        "request_id":request_id,
        "otp": otp_code,
    }
    response = client.post("/auth/2fa", json=dto)
    assert response.status_code == 401
    assert response.json["code"] is not "001"

def test_login_invalid_request_id(app, client):

    email = "paolo.rossi6@mail.it"
    request_id = "AjiUj-ssd23"
    otp_code = "A1234"
    exp_date = datetime.now(timezone.utc) + timedelta(minutes=5)

    with app.app_context():
        user = User(id=123, email = email,
                    password_hash = "acsdcdsav", 
                    name = "name", 
                    surname = "surname", 
                    age = None, 
                    use_2fv = True)

        otp = UserOtp(user_id=user.id, 
                    request_id=request_id, 
                    otp=otp_code, 
                    expiration_date=exp_date)
        db.session.add(user)
        db.session.add(otp)

        db.session.commit()

    dto = {
        "request_id":"invalid",
        "otp": otp_code,
    }
    response = client.post("/auth/2fa", json=dto)
    assert response.status_code == 401
    assert response.json["code"] is not "001"