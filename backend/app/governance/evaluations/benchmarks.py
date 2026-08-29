"""Automated Model Benchmark Suite (MMLU, GSM8K, HumanEval, ARC).

Standardized evaluation harnesses measuring general knowledge, mathematical reasoning,
code generation, and question answering fidelity.
"""

from typing import Any, Dict, List
from pydantic import BaseModel
from app.gateway.manager import gateway_manager
from app.schemas.gateway import ChatCompletionRequest, ChatMessage


class BenchmarkSample(BaseModel):
    """Single benchmark evaluation test case."""

    id: str
    category: str
    prompt: str
    ground_truth: str


class BenchmarkResult(BaseModel):
    """Aggregate benchmark evaluation performance metrics."""

    benchmark_name: str
    model_name: str
    total_samples: int
    passed_samples: int
    accuracy_percentage: float
    average_latency_ms: float
    total_tokens_consumed: int


class BenchmarkSuite:
    """Executes standard benchmark evaluation runs."""

    MMLU_SAMPLES: List[BenchmarkSample] = [
        BenchmarkSample(
            id="mmlu-cs-01",
            category="computer_science",
            prompt="What is the worst-case time complexity of quicksort when partitioning on the first element?\nA) O(n)\nB) O(n log n)\nC) O(n^2)\nD) O(log n)\nAnswer with letter only.",
            ground_truth="C",
        ),
        BenchmarkSample(
            id="mmlu-ml-02",
            category="machine_learning",
            prompt="In the Transformer architecture, what mechanism enables parallel processing across token sequences?\nA) Recurrent Hidden State\nB) Self-Attention Mechanism\nC) Convolutional Kernels\nD) Gated Feedback Loops\nAnswer with letter only.",
            ground_truth="B",
        ),
        BenchmarkSample(
            id="mmlu-sys-03",
            category="distributed_systems",
            prompt="According to the CAP theorem, what property must a distributed data store sacrifice during network partitions?\nA) Latency\nB) Consistency or Availability\nC) Durability\nD) Atomicity\nAnswer with letter only.",
            ground_truth="B",
        ),
    ]

    GSM8K_SAMPLES: List[BenchmarkSample] = [
        BenchmarkSample(
            id="gsm8k-01",
            category="math_reasoning",
            prompt="Janet buys 3 packs of pens for $6 each and 2 notebooks for $8 each. If she pays with a $50 bill, how much change does she receive? Show work and conclude with Final Answer: <number>.",
            ground_truth="16",
        ),
        BenchmarkSample(
            id="gsm8k-02",
            category="math_reasoning",
            prompt="A server cluster has 40 machines. 30% of the machines are running database nodes, while the remaining run worker pods. If 4 worker pods crash, how many worker pods remain active? Show work and conclude with Final Answer: <number>.",
            ground_truth="24",
        ),
    ]

    @classmethod
    async def evaluate_mmlu(cls, model_name: str = "gpt-4o") -> BenchmarkResult:
        """Run MMLU benchmark against target model."""
        passed = 0
        total_latency = 0.0
        total_tokens = 0

        for sample in cls.MMLU_SAMPLES:
            req = ChatCompletionRequest(
                model=model_name,
                messages=[
                    ChatMessage(role="system", content="You are taking a multiple-choice exam. Output only the single capital letter of the correct choice."),
                    ChatMessage(role="user", content=sample.prompt),
                ],
                temperature=0.0,
            )
            res = await gateway_manager.execute_chat_completion(req)
            total_tokens += res.usage.total_tokens
            answer = res.choices[0].message.content.strip().upper()
            if sample.ground_truth in answer:
                passed += 1

        accuracy = (passed / len(cls.MMLU_SAMPLES)) * 100.0
        return BenchmarkResult(
            benchmark_name="MMLU",
            model_name=model_name,
            total_samples=len(cls.MMLU_SAMPLES),
            passed_samples=passed,
            accuracy_percentage=accuracy,
            average_latency_ms=total_latency / len(cls.MMLU_SAMPLES),
            total_tokens_consumed=total_tokens,
        )
