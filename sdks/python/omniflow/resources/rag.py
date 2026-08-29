from typing import Any, Dict, List
import httpx
from omniflow.exceptions import OmniFlowSDKError

class RAGResource:
    def __init__(self, base_url: str, api_key: str, timeout: float = 60.0):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout

    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        headers = {"Authorization": f"Bearer {self.api_key}", "X-API-Key": self.api_key, "Content-Type": "application/json"}
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(f"{self.base_url}/api/v1/rag/query", headers=headers, json={"query": query_text, "top_k": top_k})
            if resp.status_code != 200:
                raise OmniFlowSDKError(f"RAG query failed: {resp.text}", resp.status_code)
            return resp.json()
