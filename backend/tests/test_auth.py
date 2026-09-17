import pytest


def test_register_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "full_name": "New Test User",
            "password": "SecurePassword123!"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["role"] == "STANDARD_USER"


def test_register_weak_password(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "weakuser@example.com",
            "full_name": "Weak User",
            "password": "password"  # No uppercase, digit, symbol
        }
    )
    assert response.status_code == 400
    assert "Password must contain at least one uppercase letter" in response.json()["detail"]


def test_login_success(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "UserPass123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["mfa_required"] is False


def test_login_invalid_password(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "WrongPassword999!"
        }
    )
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_rbac_admin_endpoint_forbidden_for_user(client, user_headers):
    response = client.get("/api/v1/admin/users", headers=user_headers)
    assert response.status_code == 403
    assert "Administrator privileges required" in response.json()["detail"]


def test_rbac_admin_endpoint_allowed_for_admin(client, admin_headers):
    response = client.get("/api/v1/admin/users", headers=admin_headers)
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 2


def test_mfa_setup_and_verify(client, user_headers):
    setup_resp = client.post("/api/v1/auth/mfa/setup", headers=user_headers)
    assert setup_resp.status_code == 200
    data = setup_resp.json()
    assert "secret" in data
    assert "qr_code_data_url" in data
    assert data["qr_code_data_url"].startswith("data:image/png;base64,")

    bad_verify = client.post("/api/v1/auth/mfa/verify", json={"code": "000000"}, headers=user_headers)
    assert bad_verify.status_code == 400

    import pyotp
    totp = pyotp.TOTP(data["secret"])
    valid_code = totp.now()
    good_verify = client.post("/api/v1/auth/mfa/verify", json={"code": valid_code}, headers=user_headers)
    assert good_verify.status_code == 200
    assert good_verify.json()["success"] is True
