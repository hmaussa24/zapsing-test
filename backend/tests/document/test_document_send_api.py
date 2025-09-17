import json
import pytest


@pytest.mark.django_db
def test_document_send_to_sign_api(client):
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
    # add one signer via API
    client.post(
        "/api/signers/",
        data=json.dumps({"document_id": doc["id"], "name": "Alice", "email": "alice@example.com"}),
        content_type="application/json",
    )

    resp = client.post(f"/api/documents/{doc['id']}/send_to_sign/")
    assert resp.status_code in (200, 202)
    body = resp.json()
    assert body.get('status') in (None, 'sent', 'created')


