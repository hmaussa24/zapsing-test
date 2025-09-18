import json
import pytest


@pytest.mark.django_db
def test_signer_api_crud(client, auth_headers, auth_company_id):
    doc = client.post(
        "/api/documents/",
        data=json.dumps({"company_id": auth_company_id, "name": "Contrato", "pdf_url": "https://e.com/a.pdf"}),
        content_type="application/json",
        **auth_headers,
    ).json()

    # create signer
    created = client.post(
        "/api/signers/",
        data=json.dumps({"document_id": doc["id"], "name": "Alice", "email": "alice@example.com"}),
        content_type="application/json",
        **auth_headers,
    )
    assert created.status_code in (200, 201)
    signer = created.json()
    assert signer["id"]

    # list by document
    lst = client.get(f"/api/signers/?document_id={doc['id']}", **auth_headers)
    assert lst.status_code == 200
    items = lst.json()
    assert isinstance(items, list) and len(items) == 1

    # delete
    delr = client.delete(f"/api/signers/{signer['id']}/", **auth_headers)
    assert delr.status_code in (200, 204)


