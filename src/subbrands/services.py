import re
from collections import defaultdict
from datetime import datetime
from typing import DefaultDict

from src.config.logging import logging
from src.core.typings import ChainBrand, SubbrandLog
from src.subbrands.repository import SubbrandRepository, subbrand_repository

logger = logging.getLogger(__name__)


class SubbrandsService:
    """Subbrands service."""

    def __init__(self, repository: SubbrandRepository) -> None:
        self.repository = repository

    def grouping_chain_brands_by_domain(
        self,
        chain_brands: list[ChainBrand],
    ) -> DefaultDict[str, list[ChainBrand]]:
        """Group chain brands by domain."""
        logger.info("Grouping chain brands by domain...")
        start_time = datetime.now()
        groups = defaultdict(list)
        for brand in chain_brands:
            groups[brand.domain_id].append(brand)
        logger.info(
            "Grouped chain brands by domain in %s",
            datetime.now() - start_time,
        )
        return groups

    def compile_synonym_patterns(
        self,
        chain_brands: list[ChainBrand],
    ) -> dict[tuple[int, str], re.Pattern]:
        """Compile chain brand patterns."""
        logger.info("Compiling chain brand patterns...")
        start_time = datetime.now()
        patterns = {}
        for brand in chain_brands:
            if (brand.id, brand.synonym) in patterns:
                continue
            patterns[(brand.id, brand.synonym)] = re.compile(
                rf"\b{re.escape(brand.synonym)}\b", re.IGNORECASE
            )
        logger.info(
            "Compiled chain brand patterns in %s",
            datetime.now() - start_time,
        )
        return patterns

    def add_subbrand_log(
        self,
        main_brand: ChainBrand,
        subbrand: ChainBrand,
    ) -> None:
        """Add subbrand log."""
        self.subbrand_logs.append(
            SubbrandLog(
                brand_id=main_brand.id,
                domain=main_brand.domain,
                synonym=main_brand.synonym,
                subbrand_id=subbrand.id,
            )
        )

    def process_search_subbrands(
        self,
        group_chain_brands: DefaultDict[str, list[ChainBrand]],
        synonym_patterns: dict[tuple[int, str], re.Pattern],
    ) -> tuple[DefaultDict[int, list[int]], list[SubbrandLog]]:
        """Process search subbrands."""
        logger.info("Processing search subbrands...")
        start_time = datetime.now()
        self.subbrand_match = set()
        self.subbrands_map = defaultdict(list)
        self.subbrand_logs = []

        for chain_brands in group_chain_brands.values():
            if len(chain_brands) < 2:
                continue

            for main_brand in chain_brands:
                if main_brand.id in self.subbrand_match:
                    continue

                main_brand_pattern = synonym_patterns[
                    (main_brand.id, main_brand.synonym)
                ]

                for subbrand in chain_brands:
                    if subbrand.id in self.subbrand_match:
                        continue

                    if subbrand.id == main_brand.id:
                        continue

                    if subbrand.actual_count >= main_brand.actual_count:
                        continue

                    subbrand_pattern: re.Pattern = synonym_patterns[
                        (subbrand.id, subbrand.synonym)
                    ]
                    if not subbrand_pattern.search(
                        main_brand.synonym
                    ) and not main_brand_pattern.search(subbrand.synonym):
                        continue

                    self.subbrand_match.add(subbrand.id)
                    self.subbrands_map[main_brand.id].append(subbrand.id)
                    self.add_subbrand_log(main_brand, subbrand)

        logger.info(
            "Processed search %d subbrands in %s",
            len(self.subbrands_map),
            datetime.now() - start_time,
        )
        return self.subbrands_map, self.subbrand_logs

    def merge_subbrands(self, subbrands_maps: DefaultDict[int, list[int]]) -> None:
        """Merge subbrands."""
        logger.info("Merging subbrands...")
        start_time = datetime.now()
        for main_brand_id, subbrand_ids in subbrands_maps.items():
            self.repository.merge_subbrands(main_brand_id, subbrand_ids)
        logger.info(
            "Merged subbrands in %s",
            datetime.now() - start_time,
        )

    def search_subbrands(self) -> list[SubbrandLog]:
        chain_brands: list[ChainBrand] = self.repository.get_chain_brands()
        group_chain_brands: DefaultDict[str, list[ChainBrand]] = (
            self.grouping_chain_brands_by_domain(chain_brands)
        )
        synonym_patterns: dict[tuple[int, str], re.Pattern] = (
            self.compile_synonym_patterns(chain_brands)
        )
        subbrands_maps, subbrand_logs = self.process_search_subbrands(
            group_chain_brands, synonym_patterns
        )
        self.merge_subbrands(subbrands_maps)
        self.repository.insert_subbrand_logs(subbrand_logs)


subbrands_service = SubbrandsService(repository=subbrand_repository)
