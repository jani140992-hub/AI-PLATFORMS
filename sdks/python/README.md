# OmniFlow AI Python SDK

Official Python client library for integrating with the OmniFlow AI Platform.

## Installation

```bash
pip install omniflow-python
```

## Quickstart

```python
from omniflow import OmniFlowClient

client = OmniFlowClient(api_key="omniflow_your_api_key")

# Chat completion
response = client.chat.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Explain quantum computing in two sentences."}],
)
print(response.choices[0].message.content)

# Streaming completion
for chunk in client.chat.create_stream(
    model="claude-3-5-sonnet-20240620",
    messages=[{"role": "user", "content": "Write a poem about distributed systems."}],
):
    print(chunk.delta, end="", flush=True)

# Run autonomous agent pipeline
agent_result = client.agents.execute(
    prompt="Design a microservices architecture for real-time payments.",
    mode="coordinator"
)
print(agent_result)
```
