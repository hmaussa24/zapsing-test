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

