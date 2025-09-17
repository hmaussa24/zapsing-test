import json
import pytest

from modules.document.application.use_cases.send_document_to_sign import SendDocumentToSignUseCase
from modules.document.application.dtos import ZapSignCreateResult
from modules.document.infrastructure.repositories.document_repository_django import DjangoDocumentRepository
from modules.company.infrastructure.repositories.company_repository_django import DjangoCompanyRepository
from modules.signer.infrastructure.repositories.signer_repository_django import DjangoSignerRepository


class FakeZapSign:
    def send_for_sign(self, api_token: str, name: str, pdf_url: str, signers: list[dict]) -> ZapSignCreateResult:
        return ZapSignCreateResult(open_id='oid', token='tok', status='sent')


@pytest.mark.django_db
def test_send_to_sign_success(client):
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

    # add one signer
    repo_sign = DjangoSignerRepository()
    repo_sign.create(document_id=doc["id"], name="Alice", email="alice@example.com")

    use_case = SendDocumentToSignUseCase(
        document_commands=DjangoDocumentRepository(),
        document_queries=DjangoDocumentRepository(),
        company_queries=DjangoCompanyRepository(),
        signer_queries=DjangoSignerRepository(),
        zap_sign_client=FakeZapSign(),
    )
    updated = use_case.execute(doc["id"])

    assert updated is not None
    assert updated.open_id == 'oid'
    assert updated.token == 'tok'
    assert updated.status == 'sent'


@pytest.mark.django_db
def test_send_to_sign_raises_when_no_signers(client):
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

    use_case = SendDocumentToSignUseCase(
        document_commands=DjangoDocumentRepository(),
        document_queries=DjangoDocumentRepository(),
        company_queries=DjangoCompanyRepository(),
        signer_queries=DjangoSignerRepository(),
        zap_sign_client=FakeZapSign(),
    )

    with pytest.raises(Exception):
        use_case.execute(doc["id"])


@pytest.mark.django_db
def test_send_to_sign_raises_when_more_than_two_signers(client):
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

    repo_sign = DjangoSignerRepository()
    repo_sign.create(document_id=doc["id"], name="A", email="a@example.com")
    repo_sign.create(document_id=doc["id"], name="B", email="b@example.com")
    # agregar un tercero
    repo_sign.create(document_id=doc["id"], name="C", email="c@example.com")

    use_case = SendDocumentToSignUseCase(
        document_commands=DjangoDocumentRepository(),
        document_queries=DjangoDocumentRepository(),
        company_queries=DjangoCompanyRepository(),
        signer_queries=DjangoSignerRepository(),
        zap_sign_client=FakeZapSign(),
    )

    with pytest.raises(Exception):
        use_case.execute(doc["id"])


