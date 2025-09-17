from modules.document.application.ports import (
    DocumentCommandRepository,
    DocumentQueryRepository,
)
from modules.document.application.use_cases.create_document import CreateDocumentUseCase
from modules.document.application.use_cases.list_documents import ListDocumentsUseCase
from modules.document.application.use_cases.get_document import GetDocumentUseCase
from modules.document.application.use_cases.update_document_partial import UpdateDocumentPartialUseCase
from modules.document.application.use_cases.delete_document import DeleteDocumentUseCase
from modules.document.infrastructure.repositories.document_repository_django import DjangoDocumentRepository
from modules.company.infrastructure.repositories.company_repository_django import DjangoCompanyRepository
from modules.document.infrastructure.adapters.zapsign_client_http import HttpZapSignClient
from modules.analysis.infrastructure.adapters.automation_notifier_http import HttpAutomationNotifier
from modules.automation.infrastructure.adapters.rabbitmq_publisher import RabbitMqEventPublisher


def get_document_command_repo() -> DocumentCommandRepository:
    return DjangoDocumentRepository()


def get_document_query_repo() -> DocumentQueryRepository:
    return DjangoDocumentRepository()


def make_create_document_use_case() -> CreateDocumentUseCase:
    return CreateDocumentUseCase(
        document_repository=get_document_command_repo(),
        company_repository=DjangoCompanyRepository(),
        zap_sign_client=HttpZapSignClient(),
        automation_notifier=HttpAutomationNotifier(),
        event_publisher=RabbitMqEventPublisher(),
    )


def make_list_documents_use_case() -> ListDocumentsUseCase:
    return ListDocumentsUseCase(document_repository=get_document_query_repo())


def make_get_document_use_case() -> GetDocumentUseCase:
    return GetDocumentUseCase(document_repository=get_document_query_repo())


def make_update_document_partial_use_case() -> UpdateDocumentPartialUseCase:
    return UpdateDocumentPartialUseCase(document_repository=get_document_command_repo())


def make_delete_document_use_case() -> DeleteDocumentUseCase:
    return DeleteDocumentUseCase(document_repository=get_document_command_repo())


