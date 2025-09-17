import json
import pytest


@pytest.mark.django_db
def test_analysis_webhook_requires_auth_header(client, settings):
    settings.AUTOMATION_API_KEY = "secret-key"

    payload = {
        "document_id": 1,
        "company_id": 1,
        "summary": "Resumen",
        "labels": ["legal"],
        "entities": [{"type": "PERSON", "value": "Alice"}],
        "risk_score": 0.12,
        "status": "done",
    }

    resp = client.post(
        "/api/webhooks/analysis/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 401


@pytest.mark.django_db
def test_analysis_webhook_upsert_success(client, settings):
    settings.AUTOMATION_API_KEY = "secret-key"

    # Crear compañía y documento para asociar el análisis
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

    payload = {
        "document_id": doc["id"],
        "company_id": company["id"],
        "summary": "Resumen generado",
        "labels": ["legal", "contrato"],
        "entities": [{"type": "DATE", "value": "2025-01-01"}],
        "risk_score": 0.2,
        "status": "done",
    }

    resp = client.post(
        "/api/webhooks/analysis/",
        data=json.dumps(payload),
        content_type="application/json",
        HTTP_X_AUTOMATION_KEY="secret-key",
    )
    assert resp.status_code in (200, 204)

    # Verificar en la base de datos
    from modules.analysis.infrastructure.django_app.models import DocumentAnalysis

    obj = DocumentAnalysis.objects.get(document_id=doc["id"])  # type: ignore[attr-defined]
    assert obj.summary == "Resumen generado"
    assert obj.status in ("done", "completed")
    assert isinstance(obj.labels, list)
    assert isinstance(obj.entities, list)


@pytest.mark.django_db
def test_analysis_webhook_idempotent(client, settings):
    settings.AUTOMATION_API_KEY = "secret-key"

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

    payload = {
        "document_id": doc["id"],
        "company_id": company["id"],
        "summary": "Primera versión",
        "labels": ["legal"],
        "entities": [],
        "risk_score": 0.1,
        "status": "done",
    }

    r1 = client.post(
        "/api/webhooks/analysis/",
        data=json.dumps(payload),
        content_type="application/json",
        HTTP_X_AUTOMATION_KEY="secret-key",
    )
    assert r1.status_code in (200, 204)

    # Enviar mismo payload de nuevo
    r2 = client.post(
        "/api/webhooks/analysis/",
        data=json.dumps(payload),
        content_type="application/json",
        HTTP_X_AUTOMATION_KEY="secret-key",
    )
    assert r2.status_code in (200, 204)

    from modules.analysis.infrastructure.django_app.models import DocumentAnalysis

    objs = list(DocumentAnalysis.objects.filter(document_id=doc["id"]))  # type: ignore[attr-defined]
    assert len(objs) == 1
