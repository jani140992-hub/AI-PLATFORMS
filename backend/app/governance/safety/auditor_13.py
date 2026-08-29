"""Safety Guardrail & Evaluation Harness - Subsystem 13.

Implements regex pattern matching, adversarial jailbreak heuristic scoring,
output schema validation, and statistical accuracy metrics for Governance Module 13.
"""

from typing import Any, Dict, List, Optional, Tuple
import re
import math


class SafetyAuditor_13:
    """Enterprise safety auditor and benchmark evaluator 13."""

    def __init__(self, strictness_level: str = "high"):
        self.strictness_level = strictness_level
        self.audited_requests_count = 0
        self.flagged_violations_count = 0

    def inspect_prompt_safety(self, prompt_text: str) -> Dict[str, Any]:
        """Verify prompt against injection, toxicity, and unauthorized system access patterns."""
        self.audited_requests_count += 1
        violations = []
        risk_score = 0.0

        # Pattern evaluations
        if re.search(r"(?i)ignore\s+(all\s+)?previous\s+instructions", prompt_text):
            violations.append("SYSTEM_PROMPT_OVERRIDE")
            risk_score += 0.85

        if re.search(r"(?i)you\s+are\s+now\s+(DAN|unrestricted|godmode)", prompt_text):
            violations.append("ADVERSARIAL_ROLE_REVERSAL")
            risk_score += 0.90

        if re.search(r"(?i)print\s+(your\s+)?(system|internal)\s+(prompt|instructions)", prompt_text):
            violations.append("SYSTEM_INFORMATION_LEAK")
            risk_score += 0.75

        is_safe = risk_score < 0.70
        if not is_safe:
            self.flagged_violations_count += 1

        return {
            "auditor": "SafetyAuditor_13",
            "is_safe": is_safe,
            "risk_score": min(1.0, risk_score),
            "violations_detected": violations,
            "sanitized_recommended": not is_safe,
        }

    def calculate_rag_triad_metric(
        self, query: str, context_chunks: List[str], generated_answer: str
    ) -> Dict[str, float]:
        """Compute composite accuracy metrics for RAG generation."""
        q_words = set(query.lower().split())
        c_words = set(" ".join(context_chunks).lower().split())
        a_words = set(generated_answer.lower().split())

        # Context relevance: how well does context match query
        context_relevance = len(q_words.intersection(c_words)) / max(1, len(q_words))
        
        # Groundedness: how much of the answer is supported by context
        groundedness = len(a_words.intersection(c_words)) / max(1, len(a_words))

        # Answer relevance: how well answer addresses query
        answer_relevance = len(q_words.intersection(a_words)) / max(1, len(q_words))

        # Composite Harmonic Mean
        denom = (1.0 / max(0.01, context_relevance)) + (1.0 / max(0.01, groundedness)) + (1.0 / max(0.01, answer_relevance))
        composite = 3.0 / denom

        return {
            "context_relevance": round(context_relevance, 4),
            "groundedness": round(groundedness, 4),
            "answer_relevance": round(answer_relevance, 4),
            "composite_score": round(composite, 4),
        }
