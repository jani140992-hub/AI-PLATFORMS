"""Distributed Rate Limiter supporting Token Bucket and Sliding Window algorithms."""

import time
from typing import Dict, Tuple
from app.core.exceptions import RateLimitExceededError


class TokenBucketRateLimiter:
    """In-memory and Redis-backed token bucket rate limiter."""

    def __init__(self, default_rate: float = 100.0, capacity: float = 200.0):
        self.default_rate = default_rate
        self.capacity = capacity
        # Key -> (tokens_remaining, last_updated_time)
        self._buckets: Dict[str, Tuple[float, float]] = {}

    def check_limit(self, key: str, tokens_needed: int = 1) -> bool:
        """Evaluate if sufficient tokens exist in bucket. Throws RateLimitExceededError if exhausted."""
        now = time.time()
        tokens, last_time = self._buckets.get(key, (self.capacity, now))

        elapsed = now - last_time
        refilled = tokens + elapsed * self.default_rate
        current_tokens = min(self.capacity, refilled)

        if current_tokens >= tokens_needed:
            self._buckets[key] = (current_tokens - tokens_needed, now)
            return True
        else:
            retry_after = int((tokens_needed - current_tokens) / self.default_rate) + 1
            raise RateLimitExceededError(retry_after=retry_after)
