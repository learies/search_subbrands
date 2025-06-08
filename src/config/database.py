import os
from typing import Any, Type

from dotenv import load_dotenv
from psycopg import Connection, connect

load_dotenv()


class DatabaseConnection:
    """Database connection class"""

    def __init__(self):
        self.connection: Connection | None = None
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL not found in environment variables")

    def connect(self) -> Connection:
        """Connect to the database with reconnect support"""
        if self.connection is None or self.connection.closed:
            self.connection = connect(self.database_url)
        return self.connection

    def close(self) -> None:
        """Close the database connection"""
        if self.connection is not None and not self.connection.closed:
            self.connection.close()
        self.connection = None

    def __enter__(self) -> Connection:
        return self.connect()

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any | None,
    ) -> None:
        if self.connection is not None and not self.connection.closed:
            if exc_type is not None and not self.connection.autocommit:
                self.connection.rollback()
            self.close()


db = DatabaseConnection()
