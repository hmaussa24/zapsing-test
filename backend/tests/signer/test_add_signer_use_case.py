import json
import pytest


@pytest.mark.django_db
def test_add_first_signer_success(client):
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

    from modules.signer.application.use_cases.add_signer_to_document import AddSignerToDocumentUseCase
    from modules.signer.application.dtos import CreateSignerDTO
    from modules.signer.infrastructure.repositories.signer_repository_django import DjangoSignerRepository

    use_case = AddSignerToDocumentUseCase(repo=DjangoSignerRepository())
    created = use_case.execute(CreateSignerDTO(document_id=doc["id"], name="Alice", email="alice@example.com"))

    assert created.id is not None
    assert created.document_id == doc["id"]
    assert created.email == "alice@example.com"


@pytest.mark.django_db
def test_add_second_signer_success(client):
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

    from modules.signer.application.use_cases.add_signer_to_document import AddSignerToDocumentUseCase
    from modules.signer.application.dtos import CreateSignerDTO
    from modules.signer.infrastructure.repositories.signer_repository_django import DjangoSignerRepository

    use_case = AddSignerToDocumentUseCase(repo=DjangoSignerRepository())
    use_case.execute(CreateSignerDTO(document_id=doc["id"], name="Alice", email="alice@example.com"))
    second = use_case.execute(CreateSignerDTO(document_id=doc["id"], name="Bob", email="bob@example.com"))

    assert second.id is not None
    assert second.email == "bob@example.com"


@pytest.mark.django_db
def test_add_third_signer_fails(client):
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

    from modules.signer.application.use_cases.add_signer_to_document import AddSignerToDocumentUseCase
    from modules.signer.application.dtos import CreateSignerDTO
    from modules.signer.infrastructure.repositories.signer_repository_django import DjangoSignerRepository

    use_case = AddSignerToDocumentUseCase(repo=DjangoSignerRepository())
    use_case.execute(CreateSignerDTO(document_id=doc["id"], name="Alice", email="alice@example.com"))
    use_case.execute(CreateSignerDTO(document_id=doc["id"], name="Bob", email="bob@example.com"))

    with pytest.raises(Exception):
        use_case.execute(CreateSignerDTO(document_id=doc["id"], name="Carol", email="carol@example.com"))


@pytest.mark.django_db
def test_add_signer_duplicate_email_fails(client):
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

    from modules.signer.application.use_cases.add_signer_to_document import AddSignerToDocumentUseCase
    from modules.signer.application.dtos import CreateSignerDTO
    from modules.signer.infrastructure.repositories.signer_repository_django import DjangoSignerRepository

    use_case = AddSignerToDocumentUseCase(repo=DjangoSignerRepository())
    use_case.execute(CreateSignerDTO(document_id=doc["id"], name="Alice", email="alice@example.com"))

    with pytest.raises(Exception):
        use_case.execute(CreateSignerDTO(document_id=doc["id"], name="Alice 2", email="alice@example.com"))


@pytest.mark.django_db
def test_add_signer_invalid_email_fails(client):
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

    from modules.signer.application.use_cases.add_signer_to_document import AddSignerToDocumentUseCase
    from modules.signer.application.dtos import CreateSignerDTO
    from modules.signer.infrastructure.repositories.signer_repository_django import DjangoSignerRepository

    use_case = AddSignerToDocumentUseCase(repo=DjangoSignerRepository())

    with pytest.raises(Exception):
        use_case.execute(CreateSignerDTO(document_id=doc["id"], name="Bad", email="not-an-email"))


