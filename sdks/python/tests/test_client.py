import pytest
from omniflow import OmniFlowClient

def test_client_initialization():
    client = OmniFlowClient(api_key="test_key", base_url="http://localhost:8000")
    assert client.api_key == "test_key"
    assert client.base_url == "http://localhost:8000"
