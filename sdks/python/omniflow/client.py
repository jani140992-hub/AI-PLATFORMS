from omniflow.resources.chat import ChatResource
from omniflow.resources.agents import AgentsResource
from omniflow.resources.rag import RAGResource
from omniflow.resources.workflows import WorkflowsResource

class OmniFlowClient:
    def __init__(self, api_key: str = "default_key", base_url: str = "http://localhost:8000", timeout: float = 60.0):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.chat = ChatResource(self.base_url, api_key, timeout)
        self.agents = AgentsResource(self.base_url, api_key, timeout)
        self.rag = RAGResource(self.base_url, api_key, timeout)
        self.workflows = WorkflowsResource(self.base_url, api_key, timeout)
