import pytest


def test_permission_payload_fuzzing(client, user_a_headers):
    fuzz_roles = ["SUPERADMIN", "ROOT", "SYSTEM", "NONE", "' OR '1'='1", "DROP TABLE users;", ""]

    for r in fuzz_roles:
        res = client.post(
            "/api/v1/permissions/1",
            json={
                "user_email": "userb@example.com",
                "role_preset": r,
                "can_view": True,
                "can_download": True
            },
            headers=user_a_headers
        )
        # Server must handle gracefully without 500 error
        assert res.status_code in [200, 201, 400, 404, 422], f"Crash on role preset fuzzing: {r}"
