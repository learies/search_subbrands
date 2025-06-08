import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "")
    RABBITMQ_QUEUE_NAME: str = os.getenv("RABBITMQ_QUEUE_NAME", "")


settings = Settings()
