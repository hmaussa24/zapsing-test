import json
import logging
from dataclasses import asdict
from typing import Optional

from django.conf import settings

from modules.automation.application.dtos import DocumentCreatedEvent
from modules.automation.application.ports import EventPublisher


logger = logging.getLogger(__name__)


class RabbitMqEventPublisher(EventPublisher):
    def __init__(self, url: Optional[str] = None, queue: Optional[str] = None) -> None:
        self.url = url or getattr(settings, 'RABBITMQ_URL', '')
        self.queue = queue or getattr(settings, 'AUTOMATION_QUEUE', 'document_created')

    def publish_document_created(self, event: DocumentCreatedEvent) -> None:
        if not self.url or not self.queue:
            logger.warning("RabbitMQ publisher disabled: missing url or queue (url=%s queue=%s)", bool(self.url), self.queue)
            return
        try:
            # Import perezoso para no requerir dependencia en pruebas sin cola
            import pika  # type: ignore
            params = pika.URLParameters(self.url)
            logger.debug("RabbitMQ connecting to %s", self.url)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.queue_declare(queue=self.queue, durable=True)
            logger.debug("RabbitMQ declared queue '%s'", self.queue)
            body = json.dumps(asdict(event)).encode('utf-8')
            channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=body,
                properties=pika.BasicProperties(delivery_mode=2),  # persistente
            )
            logger.info(
                "RabbitMQ published DocumentCreatedEvent queue=%s document_id=%s company_id=%s",
                self.queue,
                getattr(event, 'document_id', None),
                getattr(event, 'company_id', None),
            )
            channel.close()
            connection.close()
        except Exception:
            # Best-effort: no bloquear el flujo si falla la publicación
            logger.exception(
                "RabbitMQ publish failed queue=%s event=%s", self.queue, asdict(event)
            )
            return

    


