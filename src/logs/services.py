from src.core.typings import SubbrandLog
from src.logs.repository import LogRepository, log_repository


class LogService:
    """Log service."""

    def __init__(self, repository: LogRepository) -> None:
        self.repository = repository

    def create_table_subbrand_logs(self) -> None:
        """Create table subbrand logs."""
        self.repository.create_table_subbrand_logs()

    def insert_subbrand_logs(self, subbrand_logs: list[SubbrandLog]) -> None:
        """Insert subbrand logs."""
        self.create_table_subbrand_logs()
        self.repository.insert_subbrand_logs(subbrand_logs)


log_service = LogService(repository=log_repository)
