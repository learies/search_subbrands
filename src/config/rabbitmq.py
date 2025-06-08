import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError
from pika.spec import Basic, BasicProperties

from src.config.logging import logging
from src.config.settings import settings
from src.subbrands.services import subbrands_service

logger = logging.getLogger(__name__)


def get_connection_params() -> pika.ConnectionParameters:
    """Get connection parameters."""
    connection_params = pika.URLParameters(
        url=settings.RABBITMQ_URL,
    )
    connection_params.heartbeat = 10800
    return connection_params


def get_connection() -> pika.BlockingConnection:
    """Get connection."""
    return pika.BlockingConnection(
        parameters=get_connection_params(),
    )


def consume_messages(channel: "BlockingChannel") -> None:
    """Consume messages."""
    channel.queue_declare(
        queue=settings.RABBITMQ_QUEUE_NAME,
        durable=True,
    )

    def callback(
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        """Process message."""
        try:
            logger.info("Received message: %s", body)
            subbrands_service.search_subbrands()
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info("Message processed successfully")
        except Exception as e:
            logger.error("Error processing message: %s", e)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    channel.basic_consume(
        queue=settings.RABBITMQ_QUEUE_NAME,
        on_message_callback=callback,
    )
    channel.start_consuming()


def run_message_consumer() -> None:
    """Run message consumer."""
    while True:
        try:
            with get_connection() as connection:
                logger.info("Connection established")
                with connection.channel() as channel:
                    logger.info("Channel opened")
                    consume_messages(channel=channel)
        except AMQPConnectionError as e:
            logger.error(e)
            raise e
