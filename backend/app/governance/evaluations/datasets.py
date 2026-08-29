"""Prepackaged Enterprise Evaluation Datasets.

Contains structured evaluation sets for QA, code synthesis, summarization, and safety.
"""

from typing import Any, Dict, List

ENTERPRISE_QA_DATASET: List[Dict[str, Any]] = [
    {
        "id": "qa-001",
        "question": "How does OmniFlow AI handle multi-model failover when a primary provider times out?",
        "context": "The AI Gateway maintains an active circuit breaker registry. When an upstream provider times out or returns 5xx status codes exceeding the failure threshold, the state transitions to OPEN and requests are dynamically routed to healthy fallback providers specified in the priority cascade.",
        "expected_answer": "It uses an active circuit breaker registry that detects timeouts/5xx errors, transitions the provider to OPEN state, and routes to healthy fallbacks in the configured priority cascade.",
    },
    {
        "id": "qa-002",
        "question": "What algorithm does the hybrid search engine use to combine dense vector rankings and lexical BM25 rankings?",
        "context": "OmniFlow AI implements Reciprocal Rank Fusion (RRF) with a default constant k=60. Dense vector similarities and Okapi BM25 scores are converted to ranks, and a composite score is computed using the reciprocal sum.",
        "expected_answer": "It uses Reciprocal Rank Fusion (RRF) with a configurable constant (default k=60) to combine dense and BM25 rank positions into a single fused score.",
    },
    {
        "id": "qa-003",
        "question": "What is the role of the HumanApprovalNode in agent workflows?",
        "context": "The HumanApprovalNode creates an explicit pause gate within a state graph workflow. Execution state is persisted into checkpoints until an external reviewer approves or rejects the step via the web console or API.",
        "expected_answer": "It creates a pause gate that suspends workflow execution and saves state checkpoints until human review/approval is submitted.",
    },
    {
        "id": "qa-004",
        "question": "How are PII tokens masked in the governance firewall?",
        "context": "The PIIRedactor applies regular expression patterns for SSN, credit cards, emails, and phone numbers, substituting detected entities with structured tokens such as [REDACTED_SSN] before prompts reach external models.",
        "expected_answer": "Detected PII entities like SSNs or emails are replaced with structured placeholder tokens like [REDACTED_TYPE] prior to LLM forwarding.",
    },
    {
        "id": "qa-005",
        "question": "How does the semantic cache decide whether to return a cached completion?",
        "context": "Inbound prompt text is embedded into a high-dimensional vector and compared against historical queries using cosine similarity. If the similarity score exceeds the threshold (default 0.92), the cached completion is served.",
        "expected_answer": "It calculates cosine similarity between the query embedding and stored prompt embeddings; if similarity >= 0.92 (threshold), it serves the cached response.",
    },
]
