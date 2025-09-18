import json
import pytest


@pytest.mark.django_db
def test_webhook_updates_status_by_open_id(client, auth_headers, auth_company_id):
    # Crear compañía y documento
    doc = client.post(
        "/api/documents/",
        data=json.dumps({"company_id": auth_company_id, "name": "Contrato", "pdf_url": "https://e.com/a.pdf"}),
        content_type="application/json",
        **auth_headers,
    ).json()

    # Simular que el documento tiene open_id asignado por ZapSign
    from modules.document.infrastructure.django_app.models import Document as ORMDocument

    obj = ORMDocument.objects.get(id=doc["id"])  # type: ignore[attr-defined]
    obj.open_id = "oid-123"
    obj.save(update_fields=["open_id"])

    # Enviar webhook
    payload = {"open_id": "oid-123", "status": "signed"}
    resp = client.post(
        "/api/webhooks/zapsign/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code in (200, 204)

    # Verificar que el estado del documento cambió
    updated = client.get(f"/api/documents/{doc['id']}/", **auth_headers).json()
    assert updated.get("status") in ("signed", "completed")


@pytest.mark.django_db
def test_webhook_invalid_payload_returns_400(client):
    # Falta identificador
    resp = client.post(
        "/api/webhooks/zapsign/",
        data=json.dumps({"status": "signed"}),
        content_type="application/json",
    )
    assert resp.status_code in (400, 422)


@pytest.mark.django_db
def test_webhook_idempotent_same_status_twice(client, auth_headers, auth_company_id):
    doc = client.post(
        "/api/documents/",
        data=json.dumps({"company_id": auth_company_id, "name": "Contrato", "pdf_url": "https://e.com/a.pdf"}),
        content_type="application/json",
        **auth_headers,
    ).json()

    from modules.document.infrastructure.django_app.models import Document as ORMDocument
    obj = ORMDocument.objects.get(id=doc["id"])  # type: ignore[attr-defined]
    obj.open_id = "oid-456"
    obj.save(update_fields=["open_id"])

    payload = {"open_id": "oid-456", "status": "signed"}
    resp1 = client.post("/api/webhooks/zapsign/", data=json.dumps(payload), content_type="application/json")
    assert resp1.status_code in (200, 204)
    resp2 = client.post("/api/webhooks/zapsign/", data=json.dumps(payload), content_type="application/json")
    assert resp2.status_code in (200, 204)
    updated = client.get(f"/api/documents/{doc['id']}/", **auth_headers).json()
    assert updated.get("status") in ("signed", "completed")


@pytest.mark.django_db
def test_webhook_no_regression_after_signed(client, auth_headers, auth_company_id):
    doc = client.post(
        "/api/documents/",
        data=json.dumps({"company_id": auth_company_id, "name": "Contrato", "pdf_url": "https://e.com/a.pdf"}),
        content_type="application/json",
        **auth_headers,
    ).json()

    from modules.document.infrastructure.django_app.models import Document as ORMDocument
    obj = ORMDocument.objects.get(id=doc["id"])  # type: ignore[attr-defined]
    obj.open_id = "oid-789"
    obj.status = "signed"
    obj.save(update_fields=["open_id", "status"])

    # Enviar un estado inferior (pending) no debe degradar
    payload = {"open_id": "oid-789", "status": "pending"}
    resp = client.post("/api/webhooks/zapsign/", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code in (200, 204)
    updated = client.get(f"/api/documents/{doc['id']}/", **auth_headers).json()
    assert updated.get("status") in ("signed", "completed")


