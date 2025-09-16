import json
import pytest


@pytest.mark.django_db
def test_create_document_api(client):
    url = "/api/documents/"
    payload = {
        "name": "Contrato",
        "pdf_url": "https://example.com/doc.pdf"
    }
    resp = client.post(url, data=json.dumps(payload), content_type="application/json")
    assert resp.status_code in (200, 201)
    body = resp.json()
    assert body["id"] is not None
    assert body["name"] == "Contrato"
    assert body["pdf_url"] == "https://example.com/doc.pdf"

