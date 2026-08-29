"""Qdrant High-Performance Vector Database Connector."""

from typing import Any, Dict, List, Optional, Tuple
from app.rag.stores.base import BaseVectorStore
from app.core.config import settings


class QdrantVectorStore(BaseVectorStore):
    """Connector for Qdrant distributed vector search engine."""

    def __init__(self):
        self.host = settings.QDRANT_HOST
        self.port = settings.QDRANT_PORT
        # Local mock storage for simulation and tests
        self._collections: Dict[str, Dict[str, Tuple[List[float], Dict[str, Any]]]] = {}

    async def create_index(self, index_name: str, dimension: int) -> bool:
        if index_name not in self._collections:
            self._collections[index_name] = {}
        return True

    async def upsert_vectors(
        self,
        index_name: str,
        ids: List[str],
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]],
    ) -> bool:
        if index_name not in self._collections:
            self._collections[index_name] = {}
        for vid, vec, pay in zip(ids, vectors, payloads):
            self._collections[index_name][vid] = (vec, pay)
        return True

    async def search(
        self,
        index_name: str,
        query_vector: List[float],
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        if index_name not in self._collections:
            return []
        items = []
        for vid, (vec, pay) in self._collections[index_name].items():
            dot = sum(a * b for a, b in zip(query_vector, vec))
            items.append((vid, dot, pay))
        items.sort(key=lambda x: x[1], reverse=True)
        return items[:top_k]
