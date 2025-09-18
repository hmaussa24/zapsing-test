import json
import pytest


@pytest.fixture()
def auth_headers(client):
    email = "admin@acme.com"
    password = "Secret123"
    # Registrar (idempotente por email único en DB de test)
    client.post(
        "/api/auth/register",
        data=json.dumps({"name": "Acme", "email": email, "password": password, "api_token": "t"}),
        content_type="application/json",
    )
    login = client.post(
        "/api/auth/login",
        data=json.dumps({"email": email, "password": password}),
        content_type="application/json",
    )
    assert login.status_code == 200, login.content
    access = login.json()["access"]
    return {"HTTP_AUTHORIZATION": f"Bearer {access}"}


@pytest.fixture()
def auth_company_id(client, auth_headers):
    me = client.get("/api/auth/me", **auth_headers)
    assert me.status_code == 200, me.content
    return me.json()["id"]


