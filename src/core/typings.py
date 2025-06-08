from typing import NamedTuple


class ChainBrand(NamedTuple):
    id: int
    name: str
    domain_id: int
    domain: str
    synonym_id: int
    synonym: str
    actual_count: int


class SubbrandLog(NamedTuple):
    brand_id: int
    domain: str
    synonym: str
    subbrand_id: int
