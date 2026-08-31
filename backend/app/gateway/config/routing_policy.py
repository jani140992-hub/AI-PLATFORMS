"""Dynamic Routing Policy Configuration.
Defines SLA latency targets, token rate limits, and multi-provider failover matrices.
"""

GATEWAY_ROUTING_CONFIG = {
    "version": "1.2.0",
    "default_strategy": "latency_optimized",
    "fallback_chain": ["openai", "anthropic", "gemini", "deepseek"],
    "circuit_breaker": {
        "failure_threshold": 5,
        "recovery_time_seconds": 30.0,
        "half_open_max_trials": 3,
    },
    "semantic_cache": {
        "similarity_threshold": 0.92,
        "ttl_seconds": 86400,
    },
}
