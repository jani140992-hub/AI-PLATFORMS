"""OpenTelemetry Distributed Tracing Instrumentation."""

import functools
import time
from typing import Any, Callable, Dict, Optional


class MockSpan:
    """Telemetry trace span mock for recording nested execution times."""

    def __init__(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        self.name = name
        self.attributes = attributes or {}
        self.start_time = 0.0
        self.end_time = 0.0

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()

    def set_attribute(self, key: str, value: Any):
        self.attributes[key] = value


class TelemetryTracer:
    """Platform tracer for instrumenting LLM gateway and agent graphs."""

    @classmethod
    def start_span(cls, span_name: str, attributes: Optional[Dict[str, Any]] = None) -> MockSpan:
        return MockSpan(span_name, attributes)

    @classmethod
    def trace(cls, span_name: str):
        def decorator(func: Callable[..., Any]):
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any):
                with cls.start_span(span_name):
                    return await func(*args, **kwargs)
            return async_wrapper
        return decorator


tracer = TelemetryTracer()
