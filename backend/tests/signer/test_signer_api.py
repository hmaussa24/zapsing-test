import json
import pytest


@pytest.mark.django_db
def test_signer_api_crud(client):
    company = client.post(
        "/api/companies/",
        data=json.dumps({"name": "Acme", "api_token": "t"}),
        content_type="application/json",
    ).json()
    doc = client.post(
        "/api/documents/",
        data=json.dumps({"company_id": company["id"], "name": "Contrato", "pdf_url": "https://e.com/a.pdf"}),
        content_type="application/json",
    ).json()

    # create signer
    created = client.post(
        "/api/signers/",
        data=json.dumps({"document_id": doc["id"], "name": "Alice", "email": "alice@example.com"}),
        content_type="application/json",
    )
    assert created.status_code in (200, 201)
    signer = created.json()
    assert signer["id"]

    # list by document
    lst = client.get(f"/api/signers/?document_id={doc['id']}")
    assert lst.status_code == 200
    items = lst.json()
    assert isinstance(items, list) and len(items) == 1

    # delete
    delr = client.delete(f"/api/signers/{signer['id']}/")
    assert delr.status_code in (200, 204)


