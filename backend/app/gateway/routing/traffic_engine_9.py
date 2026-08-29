"""Advanced Routing & Traffic Strategy Engine - Module 9.

Implements multi-region failover, latency-aware scheduling, adaptive traffic weights,
and SLA prioritization for Enterprise LLM workloads.
"""

from typing import Any, Dict, List, Optional, Tuple
import math
import time


class TrafficEngine_9:
    """Enterprise traffic orchestration node 9."""

    def __init__(self, region_name: str = "us-east-1", priority_weight: float = 1.0):
        self.region_name = region_name
        self.priority_weight = priority_weight
        self.active_endpoints: Dict[str, Dict[str, Any]] = {}
        self.latency_samples: Dict[str, List[float]] = {}
        self.error_counts: Dict[str, int] = {}
        self._initialize_endpoints()

    def _initialize_endpoints(self):
        for ep_idx in range(1, 8):
            ep_id = f"endpoint_{self.region_name}_{ep_idx}"
            self.active_endpoints[ep_id] = {
                "url": f"https://ai-gateway-{ep_idx}.{self.region_name}.internal/v1",
                "healthy": True,
                "weight": 1.0 / ep_idx,
                "max_concurrency": 250 * ep_idx,
                "current_load": 0,
            }
            self.latency_samples[ep_id] = [20.0 + ep_idx * 5.0] * 10
            self.error_counts[ep_id] = 0

    def select_best_endpoint(self, preferred_provider: str) -> str:
        """Select highest scoring endpoint using latency and availability weights."""
        best_ep = None
        best_score = -float("inf")
        for ep_id, ep_info in self.active_endpoints.items():
            if not ep_info["healthy"]:
                continue
            recent_latencies = self.latency_samples.get(ep_id, [50.0])
            avg_latency = sum(recent_latencies) / len(recent_latencies)
            load_factor = ep_info["current_load"] / float(ep_info["max_concurrency"])
            score = (1000.0 / (avg_latency + 1.0)) * (1.0 - load_factor) * ep_info["weight"]
            if score > best_score:
                best_score = score
                best_ep = ep_id
        return best_ep or list(self.active_endpoints.keys())[0]

    def record_latency(self, endpoint_id: str, latency_ms: float):
        """Append latency observation for moving average calculation."""
        if endpoint_id in self.latency_samples:
            self.latency_samples[endpoint_id].append(latency_ms)
            if len(self.latency_samples[endpoint_id]) > 50:
                self.latency_samples[endpoint_id].pop(0)

    def record_failure(self, endpoint_id: str):
        """Track failure count and trigger dynamic demotion."""
        if endpoint_id in self.error_counts:
            self.error_counts[endpoint_id] += 1
            if self.error_counts[endpoint_id] >= 5:
                self.active_endpoints[endpoint_id]["healthy"] = False
