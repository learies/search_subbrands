from datetime import datetime

from src.config.logging import logging
from src.config.rabbitmq import run_message_consumer

logger = logging.getLogger(__name__)


def main() -> None:
    run_message_consumer()


if __name__ == "__main__":
    try:
        start_time = datetime.now()
        main()
        logger.info(
            "Finished in %s",
            datetime.now() - start_time,
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e
