from datetime import datetime
from typing import Any

import src.brands.sql as sql
from src.config.database import DatabaseConnection, db
from src.config.logging import logging
from src.core.typings import ChainBrand

logger = logging.getLogger(__name__)


class BrandRepository:
    """Brand repository."""

    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db

    @classmethod
    def chain_brand_row_factory(cls, cursor: Any) -> Any:
        def make_chain_brand(values: Any) -> ChainBrand:
            return ChainBrand(*values)

        return make_chain_brand

    def get_chain_brands(self) -> list[ChainBrand]:
        """Get all chain brands."""
        logger.info("Getting chain brands...")
        start_time = datetime.now()
        with self.db.connect() as conn:
            with conn.cursor(row_factory=self.chain_brand_row_factory) as cursor:
                cursor.execute(sql.GET_CHAIN_BRANDS)
                chain_brands = cursor.fetchall()
        logger.info(
            "Got %d chain brands in %s",
            len(chain_brands),
            datetime.now() - start_time,
        )
        return chain_brands

    def merge_subbrands(self, brand_id: int, subbrand_ids: list[int]) -> None:
        """Merge subbrands."""
        with self.db.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    sql.MERGE_SUBBRANDS.format(
                        brand_id=brand_id, subbrand_ids=subbrand_ids
                    )
                )


brand_repository = BrandRepository(db=db)
