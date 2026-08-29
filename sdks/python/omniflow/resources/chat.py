from typing import Any, Dict, Generator, List, Optional
import httpx
import json
from omniflow.types.chat import ChatCompletion, ChatStreamChunk, ChatMessageParam
from omniflow.exceptions import OmniFlowSDKError, AuthenticationError, RateLimitError

class ChatResource:
    def __init__(self, base_url: str, api_key: str, timeout: float = 60.0):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def create(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
    ) -> ChatCompletion:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(f"{self.base_url}/api/v1/chat/completions", headers=self._headers(), json=payload)
            if resp.status_code == 401:
                raise AuthenticationError("Invalid OmniFlow API key", status_code=401)
            elif resp.status_code == 429:
                raise RateLimitError("Rate limit exceeded", status_code=429)
            elif resp.status_code != 200:
                raise OmniFlowSDKError(f"Request failed: {resp.text}", status_code=resp.status_code)
            return ChatCompletion.model_validate(resp.json())

    def create_stream(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> Generator[ChatStreamChunk, None, None]:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }
        with httpx.Client(timeout=self.timeout) as client:
            with client.stream("POST", f"{self.base_url}/api/v1/chat/completions", headers=self._headers(), json=payload) as resp:
                for line in resp.iter_lines():
                    if not line.startswith("data: "):
                        continue
                    data_str = line[6:].strip()
                    if data_str == "[DONE]":
                        break
                    chunk = json.loads(data_str)
                    choice = chunk.get("choices", [{}])[0]
                    delta = choice.get("delta", {}).get("content", "")
                    finish = choice.get("finish_reason")
                    yield ChatStreamChunk(id=chunk.get("id", ""), delta=delta, finish_reason=finish)
