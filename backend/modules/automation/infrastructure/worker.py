import json
import time
import logging
from typing import Optional

from django.conf import settings

from modules.automation.application.dtos import DocumentCreatedEvent
from modules.analysis.infrastructure.adapters.automation_notifier_http import HttpAutomationNotifier


logger = logging.getLogger(__name__)


def run_worker(url: Optional[str] = None, queue: Optional[str] = None) -> None:
    amqp_url = url or getattr(settings, 'RABBITMQ_URL', '')
    qname = queue or getattr(settings, 'AUTOMATION_QUEUE', 'document_created')
    if not amqp_url or not qname:
        logger.warning('RabbitMQ not configured; worker idle')
        while True:
            time.sleep(5)

    import pika  # type: ignore
    params = pika.URLParameters(amqp_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=qname, durable=True)
    channel.basic_qos(prefetch_count=1)

    notifier = HttpAutomationNotifier()

    def _cb(ch, method, properties, body):  # type: ignore
        try:
            payload = json.loads(body.decode('utf-8'))
            ev = DocumentCreatedEvent(
                document_id=int(payload['document_id']),
                company_id=int(payload['company_id']),
                name=str(payload['name']),
                pdf_url=str(payload['pdf_url']),
            )
            logger.info('Worker received document_created id=%s', ev.document_id)
            notifier.notify_document_created(
                document_id=ev.document_id,
                company_id=ev.company_id,
                name=ev.name,
                pdf_url=ev.pdf_url,
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            # nack y requeue simple; para producción usar DLQ y backoff
            logger.exception('Worker failed processing message; nacking')
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_consume(queue=qname, on_message_callback=_cb)
    logger.info('Worker started; waiting for messages on queue=%s', qname)
    channel.start_consuming()


