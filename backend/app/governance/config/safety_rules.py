"""Zero-Trust Safety & Compliance Rule Definitions.
Configures regex PII redaction patterns, toxicity thresholds, and evaluation harnesses.
"""

SAFETY_GOVERNANCE_CONFIG = {
    "version": "1.0.0",
    "strictness_mode": "enforce",
    "pii_redaction": {
        "enabled": True,
        "mask_types": ["EMAIL", "SSN", "PHONE_NUMBER", "CREDIT_CARD", "API_KEY"],
        "replacement_token": "[REDACTED_{ENTITY_TYPE}]",
    },
    "jailbreak_firewall": {
        "adversarial_score_threshold": 0.70,
        "action_on_violation": "block_and_audit",
    },
    "benchmarks": ["MMLU", "GSM8K", "RAG_TRIAD_FAITHFULNESS"],
}
