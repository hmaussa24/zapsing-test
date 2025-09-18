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
def test_list_companies_api(client, auth_headers, auth_company_id):
    resp = client.get("/api/companies/", **auth_headers)
    assert resp.status_code == 200
    items = resp.json()
    assert isinstance(items, list)
    assert len(items) == 1
    assert items[0]["id"] == auth_company_id


@pytest.mark.django_db
def test_retrieve_company_api(client, auth_headers, auth_company_id):
    resp = client.get(f"/api/companies/{auth_company_id}/", **auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == auth_company_id


@pytest.mark.django_db
def test_update_company_api(client, auth_headers, auth_company_id):
    resp = client.patch(
        f"/api/companies/{auth_company_id}/",
        data=json.dumps({"name": "Acme Updated"}),
        content_type="application/json",
        **auth_headers,
    )
    assert resp.status_code in (200, 202)
    body = resp.json()
    assert body["id"] == auth_company_id
    assert body["name"] == "Acme Updated"


@pytest.mark.django_db
def test_delete_company_api(client, auth_headers, auth_company_id):
    resp = client.delete(f"/api/companies/{auth_company_id}/", **auth_headers)
    assert resp.status_code in (200, 204)

    resp_get = client.get(f"/api/companies/{auth_company_id}/", **auth_headers)
    assert resp_get.status_code == 404


