import json
import pytest


@pytest.mark.django_db
def test_document_send_to_sign_api(client, auth_headers, auth_company_id):
    company_id = auth_company_id
    doc = client.post(
        "/api/documents/",
        data=json.dumps({"company_id": company_id, "name": "Contrato", "pdf_url": "https://e.com/a.pdf"}),
        content_type="application/json",
        **auth_headers,
    ).json()
    # add one signer via API
    client.post(
        "/api/signers/",
        data=json.dumps({"document_id": doc["id"], "name": "Alice", "email": "alice@example.com"}),
        content_type="application/json",
        **auth_headers,
    )

    resp = client.post(f"/api/documents/{doc['id']}/send_to_sign/", **auth_headers)
    assert resp.status_code in (200, 202)
    body = resp.json()
    assert body.get('status') in (None, 'sent', 'created')


