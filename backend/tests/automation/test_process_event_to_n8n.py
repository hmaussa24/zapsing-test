from unittest.mock import Mock
from modules.automation.application.dtos import DocumentCreatedEvent
from modules.automation.application.ports import DocumentCreatedProcessor
from modules.analysis.application.ports import AutomationNotifier


class Processor(DocumentCreatedProcessor):
    def __init__(self, notifier: AutomationNotifier) -> None:
        self.notifier = notifier

    def process(self, event: DocumentCreatedEvent) -> None:
        self.notifier.notify_document_created(
            document_id=event.document_id,
            company_id=event.company_id,
            name=event.name,
            pdf_url=event.pdf_url,
        )


def test_processor_sends_to_notifier():
    notifier = Mock(spec=AutomationNotifier)
    processor = Processor(notifier)
    ev = DocumentCreatedEvent(document_id=1, company_id=2, name='Doc', pdf_url='http://e.com/a.pdf')

    processor.process(ev)

    notifier.notify_document_created.assert_called_once()


