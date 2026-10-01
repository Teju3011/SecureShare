import pytest


def test_auth_valid_login(client):
    res = client.post("/api/v1/auth/login", json={
        "email": "testadmin@example.com",
        "password": "AdminPass123!"
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_auth_invalid_password(client):
    res = client.post("/api/v1/auth/login", json={
        "email": "testadmin@example.com",
        "password": "WrongPassword!!!"
    })
    assert res.status_code == 401
    assert "Invalid email or password" in res.json()["detail"]


def test_auth_password_policy_enforcement(client):
    # Weak password without special char/uppercase
    res = client.post("/api/v1/auth/register", json={
        "email": "weakuser@example.com",
        "full_name": "Weak User",
        "password": "password"
    })
    assert res.status_code == 400


def test_auth_jwt_tamper_rejection(client):
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    res = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {fake_token}"})
    assert res.status_code == 401
