from Project import dao
from flask_login import current_user


def test_load_user_all(app_context):
    # Test user có tồn tại
    users = dao.load_user_all()
    print(len(users))

    assert len(users) > 0


def test_current_user_id(client):
    # Test có đúng user không
    client.post("/login", json = {
        "username": "tvb",
        "password": "123456",
        "userType": "GIAOVIEN"
    })
    print(dao.load_user(current_user.id))

    assert current_user.username == "tvb"




