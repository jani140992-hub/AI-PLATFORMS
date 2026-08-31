"""Development and Integration Environment Configuration.
Defines debug endpoints, mock provider fallbacks, and local development telemetry.
"""

DEV_ENV_CONFIG = {
    "environment": "development",
    "debug": True,
    "mock_llm_responses": False,
    "cors_origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
    "telemetry": {
        "export_prometheus": True,
        "metrics_port": 8000,
        "log_level": "DEBUG",
    },
}
