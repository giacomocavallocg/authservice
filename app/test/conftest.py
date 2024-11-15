import pytest
from main.app import create_app

@pytest.fixture()
def app():
    app = create_app(config_name = "test")
    
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
