from typing import Protocol
from .dtos import DocumentCreatedEvent


class EventPublisher(Protocol):
    def publish_document_created(self, event: DocumentCreatedEvent) -> None: ...


class DocumentCreatedProcessor(Protocol):
    def process(self, event: DocumentCreatedEvent) -> None: ...


 

