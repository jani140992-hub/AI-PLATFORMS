"""Multi-Agent Consensus Voting and Deliberation Protocol.

Spawns parallel independent agents, collects divergent solutions, and uses a judge agent
to vote, reconcile, and produce a high-confidence consensus output.
"""

import asyncio
from typing import Any, Dict, List
from app.gateway.manager import gateway_manager
from app.schemas.gateway import ChatCompletionRequest, ChatMessage


class ConsensusAgentDeliberation:
    """Executes multi-agent consensus generation."""

    def __init__(self, models: Optional[List[str]] = None):
        self.models = models or ["gpt-4o", "claude-3-5-sonnet-20240620", "gemini-1.5-pro"]
        self.judge_model = "gpt-4o"

    async def run_deliberation(self, question: str) -> Dict[str, Any]:
        # 1. Parallel independent inquiries
        async def call_model(model_name: str) -> Dict[str, str]:
            req = ChatCompletionRequest(
                model=model_name,
                messages=[
                    ChatMessage(role="system", content="Provide an accurate, reasoned answer with step-by-step logic."),
                    ChatMessage(role="user", content=question),
                ],
                temperature=0.3,
            )
            try:
                res = await gateway_manager.execute_chat_completion(req)
                return {"model": model_name, "response": res.choices[0].message.content}
            except Exception as e:
                return {"model": model_name, "response": f"Error: {str(e)}"}

        candidates = await asyncio.gather(*(call_model(m) for m in self.models))

        # 2. Synthesize judge prompt for consensus evaluation
        formatted_opinions = "\n\n".join([f"### Model {c['model']}:\n{c['response']}" for c in candidates])
        judge_prompt = f"""Evaluate the following independent perspectives for the question: "{question}"

Perspectives:
{formatted_opinions}

Synthesize the strongest, most factually verified consensus response, resolving any discrepancies:"""

        judge_req = ChatCompletionRequest(
            model=self.judge_model,
            messages=[
                ChatMessage(role="system", content="You are a Consensus Judge presiding over a council of AI models."),
                ChatMessage(role="user", content=judge_prompt),
            ],
            temperature=0.2,
        )
        judge_res = await gateway_manager.execute_chat_completion(judge_req)
        consensus_text = judge_res.choices[0].message.content

        return {
            "question": question,
            "individual_responses": candidates,
            "consensus_output": consensus_text,
            "participating_models": self.models,
        }
