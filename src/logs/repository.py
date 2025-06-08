from datetime import datetime

import src.logs.sql as sql
from src.config.database import DatabaseConnection, db
from src.config.logging import logging
from src.core.typings import SubbrandLog

logger = logging.getLogger(__name__)


class LogRepository:
    """Log repository."""

    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db

    def create_table_subbrand_logs(self) -> None:
        """Create table subbrand logs."""
        with self.db.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql.CHECK_TABLE_EXISTS)
                table_exists = cursor.fetchone()[0]
                if not table_exists:
                    cursor.execute(sql.CREATE_SUBBRANDS_LOG)
                    logger.warning("Table subbrand logs created")
                else:
                    logger.debug("Table subbrand logs already exists")

    def insert_subbrand_logs(self, subbrand_logs: list[SubbrandLog]) -> None:
        """Insert subbrand logs."""
        logger.info("Inserting subbrand logs...")
        start_time = datetime.now()
        with self.db.connect() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(sql.INSERT_SUBBRANDS_TO_LOG, subbrand_logs)
        logger.info(
            "Inserted %d subbrand logs in %s",
            len(subbrand_logs),
            datetime.now() - start_time,
        )


log_repository = LogRepository(db=db)
