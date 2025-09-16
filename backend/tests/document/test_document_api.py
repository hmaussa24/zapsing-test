import json
import pytest


@pytest.mark.django_db
def test_create_document_api(client):
    # crear compañía primero
    created_company = client.post(
        "/api/companies/",
        data=json.dumps({"name": "Acme", "api_token": "t"}),
        content_type="application/json",
    ).json()
    company_id = created_company["id"]

    url = "/api/documents/"
    payload = {
        "company_id": company_id,
        "name": "Contrato",
        "pdf_url": "https://example.com/doc.pdf"
    }
    resp = client.post(url, data=json.dumps(payload), content_type="application/json")
    assert resp.status_code in (200, 201)
    body = resp.json()
    assert body["id"] is not None
    assert body["name"] == "Contrato"
    assert body["pdf_url"] == "https://example.com/doc.pdf"


@pytest.mark.django_db
def test_list_documents_api(client):
    # preparar datos: company y dos documentos
    company = client.post(
        "/api/companies/",
        data=json.dumps({"name": "Acme", "api_token": "t"}),
        content_type="application/json",
    ).json()
    cid = company["id"]

    for i in range(2):
        client.post(
            "/api/documents/",
            data=json.dumps({"company_id": cid, "name": f"Doc {i}", "pdf_url": "https://e.com/d.pdf"}),
            content_type="application/json",
        )

    resp = client.get("/api/documents/")
    assert resp.status_code == 200
    items = resp.json()
    assert isinstance(items, list)
    assert len(items) >= 2


@pytest.mark.django_db
def test_retrieve_document_api(client):
    company = client.post(
        "/api/companies/",
        data=json.dumps({"name": "Acme", "api_token": "t"}),
        content_type="application/json",
    ).json()
    cid = company["id"]

    created = client.post(
        "/api/documents/",
        data=json.dumps({"company_id": cid, "name": "Contrato", "pdf_url": "https://e.com/d.pdf"}),
        content_type="application/json",
    ).json()

    resp = client.get(f"/api/documents/{created['id']}/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == created["id"]


@pytest.mark.django_db
def test_update_document_api(client):
    company = client.post(
        "/api/companies/",
        data=json.dumps({"name": "Acme", "api_token": "t"}),
        content_type="application/json",
    ).json()
    cid = company["id"]
    created = client.post(
        "/api/documents/",
        data=json.dumps({"company_id": cid, "name": "Contrato", "pdf_url": "https://e.com/d.pdf"}),
        content_type="application/json",
    ).json()

    resp = client.patch(
        f"/api/documents/{created['id']}/",
        data=json.dumps({"name": "Contrato v2"}),
        content_type="application/json",
    )
    assert resp.status_code in (200, 202)
    assert resp.json()["name"] == "Contrato v2"


@pytest.mark.django_db
def test_delete_document_api(client):
    company = client.post(
        "/api/companies/",
        data=json.dumps({"name": "Acme", "api_token": "t"}),
        content_type="application/json",
    ).json()
    cid = company["id"]
    created = client.post(
        "/api/documents/",
        data=json.dumps({"company_id": cid, "name": "Contrato", "pdf_url": "https://e.com/d.pdf"}),
        content_type="application/json",
    ).json()

    resp = client.delete(f"/api/documents/{created['id']}/")
    assert resp.status_code in (200, 204)
    assert client.get(f"/api/documents/{created['id']}/").status_code == 404

