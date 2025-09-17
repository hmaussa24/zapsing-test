import json
import pytest


@pytest.mark.django_db
def test_register_login_me_flow(client):
    # register
    reg = client.post(
        "/api/auth/register",
        data=json.dumps({"name": "Acme", "email": "admin@acme.com", "password": "Secret123"}),
        content_type="application/json",
    )
    assert reg.status_code in (200, 201)
    body = reg.json()
    assert body["id"] > 0
    assert body["name"] == "Acme"
    assert body["email"] == "admin@acme.com"

    # login
    login = client.post(
        "/api/auth/login",
        data=json.dumps({"email": "admin@acme.com", "password": "Secret123"}),
        content_type="application/json",
    )
    assert login.status_code == 200
    tokens = login.json()
    assert "access" in tokens

    # me
    me = client.get(
        "/api/auth/me",
        HTTP_AUTHORIZATION=f"Bearer {tokens['access']}"
    )
    assert me.status_code == 200
    me_body = me.json()
    assert me_body["id"] == body["id"]
    assert me_body["email"] == "admin@acme.com"
    assert me_body["name"] == "Acme"


