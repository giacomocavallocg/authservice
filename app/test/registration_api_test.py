from main.models.user import User
from main.models.context import db


def test_registration_ok(client):
    dto = {
        "email":"paolo.rossi@mail.it",
        "password": "Ab123.hhG",
        "name": "paolo",
        "surname":"rossi",
        "age": 50,
        "use2fa":True
    }
    response = client.post("/auth/registration", json=dto)
    assert response.status_code == 204

def test_registration_invalid_password(client):
    dto = {
        "email":"paolo.rossi2@mail.it",
        "password": "invalid",
        "name": "paolo",
        "surname":"rossi",
        "age": 50,
        "use2fa":True
    }
    response = client.post("/auth/registration", json=dto)
    assert response.status_code == 400
    assert response.json["code"] == "003"



def test_registration_invalid_email(client):
    dto = {
        "email":"paolo.rossimail.it",
        "password": "Ab123.hhG",
        "name": "paolo",
        "surname":"rossi",
        "age": 50,
        "use2fa":True
    }
    response = client.post("/auth/registration", json=dto)
    assert response.status_code == 400
    assert response.json["code"] == "004"


def test_registration_email_exists(app, client):

    email = "paolo.rossi3@mail.it"

    user = User(email = email,
                password_hash ="jlvhbsfdlkv", 
                name = "name", 
                surname = "surname", 
                age = None, 
                use_2fv = False)
    
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    dto = {
        "email":email,
        "password": "Ab123.hhG",
        "name": "paolo",
        "surname":"rossi",
        "age": 50,
        "use2fa":True
    }
    response = client.post("/auth/registration", json=dto)
    assert response.status_code == 400
    assert response.json["code"] == "006"