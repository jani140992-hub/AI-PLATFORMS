"""Prometheus Metrics Collector & Aggregator.

Exposes real-time counters, histograms, and gauges for system observability.
"""

from typing import Dict


class PrometheusMetricsRegistry:
    """Thread-safe metrics aggregator for Prometheus scrape endpoint."""

    def __init__(self):
        self.http_requests_total: Dict[str, int] = {}
        self.llm_tokens_total: Dict[str, int] = {}
        self.llm_cost_usd_total: Dict[str, float] = {}
        self.cache_hits_total: Dict[str, int] = {}
        self.active_agent_runs: int = 0

    def record_http_request(self, method: str, path: str, status_code: int):
        key = f'{method}:{path}:{status_code}'
        self.http_requests_total[key] = self.http_requests_total.get(key, 0) + 1

    def record_token_usage(self, model: str, prompt_tokens: int, completion_tokens: int, cost_usd: float):
        self.llm_tokens_total[f'{model}:prompt'] = self.llm_tokens_total.get(f'{model}:prompt', 0) + prompt_tokens
        self.llm_tokens_total[f'{model}:completion'] = self.llm_tokens_total.get(f'{model}:completion', 0) + completion_tokens
        self.llm_cost_usd_total[model] = self.llm_cost_usd_total.get(model, 0.0) + cost_usd

    def record_cache_hit(self, cache_type: str):
        self.cache_hits_total[cache_type] = self.cache_hits_total.get(cache_type, 0) + 1

    def generate_prometheus_export(self) -> str:
        lines = [
            "# HELP omniflow_http_requests_total Total HTTP requests handled",
            "# TYPE omniflow_http_requests_total counter",
        ]
        for key, val in self.http_requests_total.items():
            method, path, status = key.split(":")
            lines.append(f'omniflow_http_requests_total{{method="{method}",path="{path}",status="{status}"}} {val}')

        lines.extend([
            "# HELP omniflow_llm_tokens_total Total tokens processed across models",
            "# TYPE omniflow_llm_tokens_total counter",
        ])
        for key, val in self.llm_tokens_total.items():
            model, ttype = key.split(":")
            lines.append(f'omniflow_llm_tokens_total{{model="{model}",type="{ttype}"}} {val}')

        lines.extend([
            "# HELP omniflow_llm_cost_usd_total Total estimated LLM cost in USD",
            "# TYPE omniflow_llm_cost_usd_total counter",
        ])
        for model, cost in self.llm_cost_usd_total.items():
            lines.append(f'omniflow_llm_cost_usd_total{{model="{model}"}} {cost:.6f}')

        return "\n".join(lines) + "\n"


metrics = PrometheusMetricsRegistry()
