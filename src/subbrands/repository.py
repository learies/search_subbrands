from src.brands.repository import brand_repository
from src.core.repository import Repository
from src.core.typings import ChainBrand, SubbrandLog
from src.logs.repository import log_repository


class SubbrandRepository(Repository):
    """Subbrand repository."""

    def get_chain_brands(self) -> list[ChainBrand]:
        """Get all chain brands."""
        return brand_repository.get_chain_brands()

    def merge_subbrands(self, main_brand_id: int, subbrand_ids: list[int]) -> None:
        """Merge subbrands."""
        brand_repository.merge_subbrands(main_brand_id, subbrand_ids)

    def create_table_subbrand_logs(self) -> None:
        """Create table subbrand logs."""
        log_repository.create_table_subbrand_logs()

    def insert_subbrand_logs(self, subbrand_logs: list[SubbrandLog]) -> None:
        """Insert subbrand logs."""
        self.create_table_subbrand_logs()
        log_repository.insert_subbrand_logs(subbrand_logs)


subbrand_repository = SubbrandRepository()
