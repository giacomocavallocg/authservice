from main.models.otp import UserOtp

def test_registration(client):
    registration_dto = {
        "email":"paolo.rossi10@mail.it",
        "password": "Ab123.hhG",
        "name": "paolo",
        "surname":"rossi",
        "age": 50,
        "use2fa":False
    }
    response = client.post("/auth/registration", json=registration_dto)
    assert response.status_code == 204

    login_dto = {
        "email": registration_dto["email"],
        "password": registration_dto["password"],
    }

    response = client.post("/auth/login", json=login_dto)
    assert response.status_code == 200

    token = response.json["token"]
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = client.get("/users/me", headers = headers)
    assert response.status_code == 200
    assert response.json["email"] == registration_dto["email"]


def test_registration_2fa(app, client):
    registration_dto = {
        "email":"paolo.rossi11@mail.it",
        "password": "Ab123.hhG",
        "name": "paolo",
        "surname":"rossi",
        "age": 50,
        "use2fa":True
    }
    response = client.post("/auth/registration", json=registration_dto)
    assert response.status_code == 204

    login_dto = {
        "email": registration_dto["email"],
        "password": registration_dto["password"],
    }

    response = client.post("/auth/login", json=login_dto)
    assert response.status_code == 200

    otp_code = None
    with app.app_context():
        otp = UserOtp.query.filter(UserOtp.request_id == response.json["request_id"]).one()
        assert otp is not None
        otp_code = otp.otp
    
    
    dto = {
        "request_id": response.json["request_id"],
        "otp": otp_code,
    }
    response = client.post("/auth/2fa", json=dto)
    assert response.status_code == 200
    
    token = response.json["token"]
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = client.get("/users/me", headers = headers)
    assert response.status_code == 200
    assert response.json["email"] == registration_dto["email"]