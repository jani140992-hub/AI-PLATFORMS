from typing import Any, Dict
import httpx
from omniflow.exceptions import OmniFlowSDKError

class WorkflowsResource:
    def __init__(self, base_url: str, api_key: str, timeout: float = 120.0):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout

    def run(self, workflow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.api_key}", "X-API-Key": self.api_key, "Content-Type": "application/json"}
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(f"{self.base_url}/api/v1/workflows/run", headers=headers, json={"workflow_id": workflow_id, "inputs": inputs})
            if resp.status_code != 200:
                raise OmniFlowSDKError(f"Workflow run failed: {resp.text}", resp.status_code)
            return resp.json()
