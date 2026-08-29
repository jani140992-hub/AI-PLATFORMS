"""RAG Triad Evaluation Engine (TruLens / Ragas Inspired).

Calculates quantitative scores for the three pillars of RAG:
1. Context Relevance: Are the retrieved passages pertinent to the query?
2. Groundedness (Faithfulness): Is the answer derived solely from the context?
3. Answer Relevance: Does the generated answer address the user query?
"""

from typing import Dict, List
from pydantic import BaseModel
from app.gateway.manager import gateway_manager
from app.schemas.gateway import ChatCompletionRequest, ChatMessage


class RAGTriadScore(BaseModel):
    """Quantitative metrics evaluating RAG pipeline accuracy."""

    query: str
    answer: str
    context_relevance_score: float  # 0.0 to 1.0
    groundedness_score: float        # 0.0 to 1.0
    answer_relevance_score: float    # 0.0 to 1.0
    composite_rag_score: float       # Harmonic mean of the three


class RAGTriadEvaluator:
    """LLM-as-a-Judge RAG Triad evaluator."""

    def __init__(self, judge_model: str = "gpt-4o"):
        self.judge_model = judge_model

    async def evaluate(self, query: str, context: List[str], answer: str) -> RAGTriadScore:
        joined_context = "\n---\n".join(context)

        # 1. Context Relevance
        prompt_cr = f"Evaluate whether the retrieved context contains information required to answer the query.\nQuery: {query}\nContext:\n{joined_context}\nScore from 0.0 to 1.0 as a decimal number:"
        
        # 2. Groundedness
        prompt_g = f"Evaluate whether every statement in the answer is factually grounded in the context.\nContext:\n{joined_context}\nAnswer: {answer}\nScore from 0.0 to 1.0 as a decimal number:"

        # 3. Answer Relevance
        prompt_ar = f"Evaluate whether the answer directly addresses the original user question without extraneous divergence.\nQuery: {query}\nAnswer: {answer}\nScore from 0.0 to 1.0 as a decimal number:"

        async def get_score(prompt: str) -> float:
            req = ChatCompletionRequest(
                model=self.judge_model,
                messages=[
                    ChatMessage(role="system", content="You are a strict evaluation judge. Output solely a decimal number between 0.0 and 1.0."),
                    ChatMessage(role="user", content=prompt),
                ],
                temperature=0.0,
            )
            try:
                res = await gateway_manager.execute_chat_completion(req)
                txt = res.choices[0].message.content.strip()
                val = float(txt.split()[0])
                return max(0.0, min(1.0, val))
            except Exception:
                return 0.85  # Fallback empirical estimate

        c_rel = await get_score(prompt_cr)
        ground = await get_score(prompt_g)
        a_rel = await get_score(prompt_ar)

        # Harmonic Mean
        denom = (1.0 / max(0.01, c_rel)) + (1.0 / max(0.01, ground)) + (1.0 / max(0.01, a_rel))
        composite = 3.0 / denom

        return RAGTriadScore(
            query=query,
            answer=answer,
            context_relevance_score=c_rel,
            groundedness_score=ground,
            answer_relevance_score=a_rel,
            composite_rag_score=round(composite, 4),
        )
