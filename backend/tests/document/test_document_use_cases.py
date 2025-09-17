import json
import pytest

from modules.document.application.use_cases.list_documents import ListDocumentsUseCase
from modules.document.application.use_cases.get_document import GetDocumentUseCase
from modules.document.application.use_cases.update_document_partial import UpdateDocumentPartialUseCase
from modules.document.application.use_cases.delete_document import DeleteDocumentUseCase
from modules.document.application.use_cases.create_document import CreateDocumentUseCase
from modules.document.application.dtos import CreateDocumentDTO
from modules.document.infrastructure.repositories.document_repository_django import DjangoDocumentRepository


@pytest.mark.django_db
def test_usecase_list_documents_by_company(client):
    # crear compañía
    company = client.post(
        "/api/companies/",
        data=json.dumps({"name": "Acme", "api_token": "t"}),
        content_type="application/json",
    ).json()
    cid = company["id"]

    repo = DjangoDocumentRepository()
    # crear 2 documentos
    CreateDocumentUseCase(repo).execute(CreateDocumentDTO(company_id=cid, name="A", pdf_url="https://e.com/a.pdf"))
    CreateDocumentUseCase(repo).execute(CreateDocumentDTO(company_id=cid, name="B", pdf_url="https://e.com/b.pdf"))

    page = ListDocumentsUseCase(repo).execute(company_id=cid)
    assert page.count == 2
    assert len(page.results) == 2
    # orden desc por created_at: último creado primero
    assert page.results[0].name == "B"


@pytest.mark.django_db
def test_usecase_get_update_delete_document(client):
    company = client.post(
        "/api/companies/",
        data=json.dumps({"name": "Acme", "api_token": "t"}),
        content_type="application/json",
    ).json()
    cid = company["id"]

    repo = DjangoDocumentRepository()
    created = CreateDocumentUseCase(repo).execute(CreateDocumentDTO(company_id=cid, name="X", pdf_url="https://e.com/x.pdf"))

    got = GetDocumentUseCase(repo).execute(created.id)
    assert got is not None and got.id == created.id

    updated = UpdateDocumentPartialUseCase(repo).execute(created.id, name="Y")
    assert updated is not None and updated.name == "Y"

    ok = DeleteDocumentUseCase(repo).execute(created.id)
    assert ok is True
    assert GetDocumentUseCase(repo).execute(created.id) is None


