"""Pre-Production Staging Environment Configuration.
Defines staging cluster thresholds, load testing parameters, and canary configs.
"""

STAGING_ENV_CONFIG = {
    "environment": "staging",
    "debug": False,
    "cluster_replicas": 4,
    "autoscaling": {
        "min_replicas": 2,
        "max_replicas": 10,
        "target_cpu_utilization": 70,
    },
    "canary_traffic_percent": 10,
}
