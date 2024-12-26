import pytest
from Project import create_app, admin


@pytest.fixture()
def app():
    app = create_app()

    yield app


@pytest.fixture
def app_context():
    app = create_app()  # Tạo một instance của ứng dụng Flask
    with app.app_context():
        yield

@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client
