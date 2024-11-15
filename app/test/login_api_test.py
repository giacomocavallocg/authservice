from main.models.user import User
from main.models.context import db
from main.services import psw_hasher


def test_login_ok(app, client):

    email = "paolo.rossi4@mail.it"
    psw = "AjiUj-ssd23"
    with app.app_context():
        user = User(email = email,
                    password_hash =psw_hasher.hash_password(psw), 
                    name = "name", 
                    surname = "surname", 
                    age = None, 
                    use_2fv = False)
    
        db.session.add(user)
        db.session.commit()

    dto = {
        "email":email,
        "password": psw,
    }
    response = client.post("/auth/login", json=dto)
    assert response.status_code == 200
    assert "token" in response.json
    assert response.json["token"] is not None


def test_login_2fa_ok(app, client):

    email = "paolo.rossi5@mail.it"
    psw = "AjiUj-ssd23"
    with app.app_context():
        user = User(email = email,
                    password_hash =psw_hasher.hash_password(psw), 
                    name = "name", 
                    surname = "surname", 
                    age = None, 
                    use_2fv = True)
    
        db.session.add(user)
        db.session.commit()

    dto = {
        "email":email,
        "password": psw,
    }
    response = client.post("/auth/login", json=dto)
    assert response.status_code == 200
    assert "request_id" in response.json
    assert "validation_endpoint" in response.json
    assert response.json["request_id"] is not None
    assert response.json["validation_endpoint"] is not None


def test_login_invalid_email(app, client):

    email = "not-exists@mail.it"
    psw = "AjiUj-ssd23"
    dto = {
        "email":email,
        "password": psw,
    }
    response = client.post("/auth/login", json=dto)
    assert response.status_code == 401
    assert response.json["code"] == "001"

def test_login_invalid_psw(app, client):

    email = "paolo.rossi5@mail.it"
    psw = "AjiUj-ssd23"
    with app.app_context():
        user = User(email = email,
                    password_hash =psw_hasher.hash_password(psw), 
                    name = "name", 
                    surname = "surname", 
                    age = None, 
                    use_2fv = False)
    
        db.session.add(user)
        db.session.commit()

    dto = {
        "email":email,
        "password": "invalid-psw",
    }
    response = client.post("/auth/login", json=dto)
    assert response.status_code == 401
    assert response.json["code"] == "001"