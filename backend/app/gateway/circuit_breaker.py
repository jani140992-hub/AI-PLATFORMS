"""Distributed Circuit Breaker with Half-Open State Probing.

Prevents cascading outages when upstream model providers experience high error rates
or latency degradation.
"""

from datetime import datetime, timezone
from enum import Enum
import threading
import time
from typing import Dict, Optional


class CircuitState(str, Enum):
    CLOSED = "closed"        # Operating normally, routing traffic
    OPEN = "open"            # Failing, traffic blocked / redirected to fallback
    HALF_OPEN = "half_open"  # Probing upstream health with limited canary traffic


class CircuitBreaker:
    """Thread-safe circuit breaker maintaining state per model provider."""

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_seconds: float = 30.0,
        half_open_success_threshold: int = 2,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self.half_open_success_threshold = half_open_success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self._lock = threading.Lock()

    def allow_request(self) -> bool:
        """Evaluate whether a new request should be permitted to execute."""
        with self._lock:
            now = time.time()
            if self.state == CircuitState.CLOSED:
                return True
            elif self.state == CircuitState.OPEN:
                if self.last_failure_time and (now - self.last_failure_time >= self.recovery_timeout_seconds):
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                    return True
                return False
            elif self.state == CircuitState.HALF_OPEN:
                return True
        return False

    def record_success(self):
        """Record a successful provider invocation."""
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.half_open_success_threshold:
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    self.success_count = 0
            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0

    def record_failure(self):
        """Record a provider error or timeout."""
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.state == CircuitState.CLOSED and self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            elif self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN


class CircuitBreakerRegistry:
    """Registry maintaining circuit breakers for all registered providers."""

    _breakers: Dict[str, CircuitBreaker] = {}
    _lock = threading.Lock()

    @classmethod
    def get_breaker(cls, provider_name: str) -> CircuitBreaker:
        with cls._lock:
            if provider_name not in cls._breakers:
                cls._breakers[provider_name] = CircuitBreaker(name=provider_name)
            return cls._breakers[provider_name]
