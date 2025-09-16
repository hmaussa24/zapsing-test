import json
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_company_api(client, settings):
    url = "/api/companies/"
    payload = {"name": "Acme Corp", "api_token": "token-123"}
    response = client.post(url, data=json.dumps(payload), content_type="application/json")
    assert response.status_code in (200, 201)
    body = response.json()
    assert body.get("id") is not None
    assert body["name"] == "Acme Corp"
    assert body["api_token"] == "token-123"


@pytest.mark.django_db
def test_list_companies_api(client):
    # crear dos compañías
    client.post("/api/companies/", data=json.dumps({"name": "A", "api_token": "t1"}), content_type="application/json")
    client.post("/api/companies/", data=json.dumps({"name": "B", "api_token": "t2"}), content_type="application/json")

    resp = client.get("/api/companies/")
    assert resp.status_code == 200
    items = resp.json()
    assert isinstance(items, list)
    assert len(items) >= 2
    names = {i["name"] for i in items}
    assert {"A", "B"}.issubset(names)


@pytest.mark.django_db
def test_retrieve_company_api(client):
    created = client.post("/api/companies/", data=json.dumps({"name": "Acme", "api_token": "t"}), content_type="application/json").json()
    company_id = created["id"]

    resp = client.get(f"/api/companies/{company_id}/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == company_id
    assert body["name"] == "Acme"


@pytest.mark.django_db
def test_update_company_api(client):
    created = client.post(
        "/api/companies/",
        data=json.dumps({"name": "Acme", "api_token": "t"}),
        content_type="application/json",
    ).json()
    company_id = created["id"]

    resp = client.patch(
        f"/api/companies/{company_id}/",
        data=json.dumps({"name": "Acme Updated"}),
        content_type="application/json",
    )
    assert resp.status_code in (200, 202)
    body = resp.json()
    assert body["id"] == company_id
    assert body["name"] == "Acme Updated"


@pytest.mark.django_db
def test_delete_company_api(client):
    created = client.post(
        "/api/companies/",
        data=json.dumps({"name": "ToDelete", "api_token": "t"}),
        content_type="application/json",
    ).json()
    company_id = created["id"]

    resp = client.delete(f"/api/companies/{company_id}/")
    assert resp.status_code in (200, 204)

    resp_get = client.get(f"/api/companies/{company_id}/")
    assert resp_get.status_code == 404


