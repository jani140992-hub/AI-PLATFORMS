"""Abstract Vector Database Store Interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple


class BaseVectorStore(ABC):
    """Abstract vector database connector."""

    @abstractmethod
    async def create_index(self, index_name: str, dimension: int) -> bool:
        pass

    @abstractmethod
    async def upsert_vectors(
        self,
        index_name: str,
        ids: List[str],
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]],
    ) -> bool:
        pass

    @abstractmethod
    async def search(
        self,
        index_name: str,
        query_vector: List[float],
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        pass
