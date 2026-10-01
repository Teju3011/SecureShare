import pytest

API_FUZZ_INPUTS = [
    -1, 0, 999999999999999999, "NaN", "Infinity", "-Infinity",
    "' UNION SELECT null, null, null--",
    "<svg onload=alert(1)>",
    "true", "false", "undefined", "null"
]


def test_api_param_fuzzing(client, user_a_headers):
    for val in API_FUZZ_INPUTS:
        # Fuzz search/filter endpoints
        res = client.get(f"/api/v1/files?q={val}", headers=user_a_headers)
        assert res.status_code in [200, 400, 422], f"Crash on search query: {val}"


def test_share_token_fuzzing(client):
    for val in API_FUZZ_INPUTS:
        res = client.get(f"/api/v1/shares/public/{val}")
        assert res.status_code in [404, 400, 422], f"Crash on share token: {val}"
