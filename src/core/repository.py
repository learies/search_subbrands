from typing import Protocol

from src.core.typings import ChainBrand, SubbrandLog


class Repository(Protocol):
    """Subbrands repository."""

    def get_chain_brands(self) -> list[ChainBrand]:
        """Get all subbrands."""
        return []

    def merge_subbrands(self, main_brand_id: int, subbrand_ids: list[int]) -> None:
        """Merge subbrands."""
        pass

    def insert_subbrand_logs(self, subbrand_logs: list[SubbrandLog]) -> None:
        """Insert subbrand logs."""
        pass
