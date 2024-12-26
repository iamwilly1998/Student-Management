def test_login_page(client):
    response = client.get("/", follow_redirects=True)
    print(response.data)
    assert b"<title>Login</title>" in response.data


def test_login_fail(client):
    # Test đăng nhập
    response = client.post("/login", json = {
        "username": "saitaikhoan",
        "password": "passsai",
        "userType": "NHANVIEN"
    }, follow_redirects = True)
    assert "Đăng nhập thất bại" in response.data.decode('utf-8')


def test_nhanvien_login_logout(client):
    # Test đăng nhập
    response = client.post("/login", json={
        "username": "ndmh",
        "password": "123456",
        "userType": "NHANVIEN"
    }, follow_redirects=True)
    assert "Xin chào nhân viên" in response.data.decode('utf-8')

    # Test đăng xuất
    logout_response = client.get("/logout", follow_redirects = True)
    assert b"<title>Login</title>" in logout_response.data


def test_admin_login_logout(client):
    # Test đăng nhập
    response = client.post("/login", json={
        "username": "ndmh",
        "password": "123456",
        "userType": "ADMIN"
    }, follow_redirects=True)
    assert "QUẢN TRỊ VIÊN" in response.data.decode('utf-8')

    # Test đăng xuất
    logout_response = client.get("/admin/mylogoutview", follow_redirects = True)
    assert b"<title>Login</title>" in logout_response.data

def test_giaovien_login(client):
    # Test đăng nhập
    response = client.post("/login", json={
        "username": "tvb",
        "password": "123456",
        "userType": "GIAOVIEN"
    }, follow_redirects=True)
    assert "Xin chào giáo viên" in response.data.decode('utf-8')

    # Test đăng xuất
    logout_response = client.get("/logout", follow_redirects = True)
    assert b"<title>Login</title>" in logout_response.data


def test_nhanvien_access_ability(client):
    # Test đăng nhập tài khoản NHANVIEN sau đó vào được quản lý sinh viên
    # Và không vào được trang của role khác
    client.post("/login", json = {
        "username": "ndmh",
        "password": "123456",
        "userType": "NHANVIEN"
    })

    manage_response = client.get("/nhanvien/quan_ly_sinh_vien")
    assert manage_response.status_code == 200

    input_score_response = client.get("/giaovien/xuat_diem")
    assert input_score_response.status_code != 200


def test_giaovien_access_ability(client):
    # Test đăng nhập tài khoản GIAOVIEN sau đó không vào được quản lý sinh viên
    # Chỉ vào được xuất điểm, nhập điểm của mình
    client.post("/login", json={
        "username": "tvb",
        "password": "123456",
        "userType": "GIAOVIEN"
    })

    manage_response = client.get("/nhanvien/quan_ly_sinh_vien")
    assert manage_response.status_code != 200

    input_score_response = client.get("/giaovien/xuat_diem")
    assert input_score_response.status_code == 200