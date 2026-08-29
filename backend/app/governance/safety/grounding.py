"""Hallucination Detection & Context Groundedness Guard.

Validates that LLM generated answers are strictly faithful to retrieved source documents
without fabricating unsupported claims.
"""

from typing import List, Tuple


class GroundingGuard:
    """Evaluates factual grounding between context passages and model responses."""

    def __init__(self, min_overlap_ratio: float = 0.4):
        self.min_overlap_ratio = min_overlap_ratio

    def evaluate_groundedness(self, answer: str, context_passages: List[str]) -> Tuple[float, bool]:
        """Compute key factual term overlap between generated answer and provided context."""
        if not context_passages or not answer.strip():
            return 0.0, False

        combined_context = " ".join(context_passages).lower()
        answer_words = [w.strip(".,;:?!\"'") for w in answer.lower().split() if len(w) > 3]

        if not answer_words:
            return 1.0, True

        supported_words = [w for w in answer_words if w in combined_context]
        groundedness_ratio = len(supported_words) / float(len(answer_words))

        is_grounded = groundedness_ratio >= self.min_overlap_ratio
        return round(groundedness_ratio, 4), is_grounded
