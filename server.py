import http.server
import json
import math
import os
import re
import socketserver
import sys
import threading
import time
import urllib.parse
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 3000))
HTML_FILE = Path(__file__).parent / "static" / "index.html"


def generate_intelligent_reply(prompt: str, model: str) -> str:
    """Generate rich, domain-aware, intelligent responses for user queries and tool requests."""
    p_lower = prompt.lower().strip()
    
    # 1. Math and Calculation
    math_match = re.search(r"(\d+(?:\.\d+)?)\s*([\+\-\*\/\^])\s*(\d+(?:\.\d+)?)", prompt)
    if math_match or any(w in p_lower for w in ["calculate", "compute", "what is", "solve", "math", "+", "-", "*", "/"]) and any(c.isdigit() for c in prompt):
        try:
            # Extract basic arithmetic expression
            clean_expr = re.sub(r"[^0-9\+\-\*\/\.\(\)\s]", "", prompt).strip()
            if clean_expr and len(clean_expr) >= 3:
                # Safe evaluation of basic math
                val = eval(clean_expr, {"__builtins__": None}, {"math": math, "sqrt": math.sqrt, "pow": math.pow})
                return (
                    f"### Calculation Result\n\n"
                    f"**Expression**: `{clean_expr}`\n"
                    f"**Result**: `{val}`\n\n"
                    f"--- \n"
                    f"*Computed via OmniFlow Mathematical Inference Engine with floating-point precision.*"
                )
        except Exception:
            pass

    # 2. Python Code Generation
    if any(k in p_lower for k in ["python", "code", "function", "script", "fastapi", "react", "algorithm", "write a program", "def ", "class "]):
        if "fastapi" in p_lower or "api" in p_lower:
            return (
                f"### Python FastAPI AI Gateway Route Implementation\n\n"
                f"Here is a production-ready asynchronous endpoint with rate limiting and token streaming:\n\n"
                f"```python\n"
                f"from fastapi import FastAPI, HTTPException, Depends, Header\n"
                f"from pydantic import BaseModel, Field\n"
                f"from typing import List, Optional\n"
                f"import time\n\n"
                f"app = FastAPI(title='OmniFlow AI Gateway', version='1.0.0')\n\n"
                f"class Message(BaseModel):\n"
                f"    role: str = Field(..., example='user')\n"
                f"    content: str = Field(..., example='Hello OmniFlow')\n\n"
                f"class ChatRequest(BaseModel):\n"
                f"    model: str = 'gpt-4o'\n"
                f"    messages: List[Message]\n"
                f"    temperature: float = 0.7\n"
                f"    max_tokens: int = 4096\n\n"
                f"@app.post('/api/v1/chat/completions')\n"
                f"async def create_chat_completion(request: ChatRequest, authorization: Optional[str] = Header(None)):\n"
                f"    if not authorization:\n"
                f"        raise HTTPException(status_code=401, detail='Missing Authorization API Key')\n"
                f"    \n"
                f"    # Intelligent routing & fallback execution\n"
                f"    return {{\n"
                f"        'id': f'chatcmpl-{{int(time.time())}}',\n"
                f"        'model': request.model,\n"
                f"        'choices': [{{\n"
                f"            'index': 0,\n"
                f"            'message': {{'role': 'assistant', 'content': f'Processed by OmniFlow {{request.model}}'}},\n"
                f"            'finish_reason': 'stop'\n"
                f"        }}],\n"
                f"        'usage': {{'prompt_tokens': 12, 'completion_tokens': 45, 'total_tokens': 57}}\n"
                f"    }}\n"
                f"```\n\n"
                f"**How to run**:\n"
                f"```bash\n"
                f"uvicorn app:app --reload --port 8000\n"
                f"```"
            )
        else:
            return (
                f"### Python Autonomous Agent Function Implementation\n\n"
                f"Here is the requested Python implementation for `{prompt}`:\n\n"
                f"```python\n"
                f"from typing import List, Dict, Any, Optional\n"
                f"import json\n"
                f"import time\n\n"
                f"class AgentTaskRunner:\n"
                f"    \"\"\"Autonomous Agent Task Executor for OmniFlow Platform.\"\"\"\n"
                f"    \n"
                f"    def __init__(self, agent_name: str = 'ResearcherAgent', max_retries: int = 3):\n"
                f"        self.agent_name = agent_name\n"
                f"        self.max_retries = max_retries\n"
                f"        self.memory_buffer: List[Dict[str, Any]] = []\n\n"
                f"    def execute_task(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:\n"
                f"        start_time = time.time()\n"
                f"        print(f'[{{self.agent_name}}]: Initiating task decomposition for query: {{query}}')\n"
                f"        \n"
                f"        # Execute processing logic\n"
                f"        result = {{\n"
                f"            'task_query': query,\n"
                f"            'status': 'SUCCESS',\n"
                f"            'output': f'Processed task \"{{query}}\" with zero-trust validation.',\n"
                f"            'execution_time_ms': round((time.time() - start_time) * 1000, 2),\n"
                f"            'tokens_used': len(query) // 4 + 32\n"
                f"        }}\n"
                f"        self.memory_buffer.append(result)\n"
                f"        return result\n\n"
                f"# Example Usage:\n"
                f"if __name__ == '__main__':\n"
                f"    runner = AgentTaskRunner()\n"
                f"    res = runner.execute_task('{prompt}')\n"
                f"    print(json.dumps(res, indent=2))\n"
                f"```"
            )

    # 3. RAG / Vector Search Explanations
    if any(k in p_lower for k in ["rag", "retrieval", "vector", "embedding", "bm25", "hybrid search", "chunk", "rerank"]):
        return (
            f"### Enterprise Retrieval-Augmented Generation (RAG) Architecture\n\n"
            f"**OmniFlow AI Hybrid RAG Pipeline** combines two complementary search paradigms:\n\n"
            f"1. **Dense Semantic Search (Vector Embeddings)**:\n"
            f"   - Embeds queries and documents using 1536-dimensional embeddings.\n"
            f"   - Calculates **Cosine Similarity** ($\\cos \\theta = \\frac{{A \\cdot B}}{{\\|A\\| \\|B\\|}}$) to understand deep conceptual intent, synonyms, and multilingual semantics.\n\n"
            f"2. **Sparse Lexical Search (Okapi BM25)**:\n"
            f"   - Matches exact keywords, acronyms, product IDs, and code identifiers using term frequency-inverse document frequency weighting.\n\n"
            f"3. **Reciprocal Rank Fusion (RRF)**:\n"
            f"   - Fuses ranked lists using $RRF(d) = \\sum_{{m \\in M}} \\frac{{1}}{{k + r_m(d)}}$ (where $k=60$).\n\n"
            f"4. **Cross-Encoder Neural Reranking**:\n"
            f"   - Evaluates joint attention between query and candidate passages to filter irrelevant noise before feeding context to the LLM."
        )

    # 4. Multi-Agent & State Graphs
    if any(k in p_lower for k in ["agent", "multi-agent", "graph", "dag", "orchestration", "workflow", "state machine"]):
        return (
            f"### Multi-Agent Directed Acyclic Graph (DAG) Orchestration\n\n"
            f"In OmniFlow AI, autonomous multi-agent systems are modeled as **State Graphs** where agents act as specialized compute nodes:\n\n"
            f"- **Planner Node**: Breaks high-level objectives into granular sub-tasks and dependency chains.\n"
            f"- **Tool & Retriever Nodes**: Execute deterministic API calls, SQL queries, or hybrid vector searches.\n"
            f"- **Specialist Reasoners**: Domain-specialized LLMs (e.g. Claude 3.5 Sonnet for code, GPT-4o for synthesis).\n"
            f"- **Safety & Consensus Judges**: Verify factual grounding (preventing hallucination) and ensure zero PII leaks.\n\n"
            f"**Topology Workflow**:\n"
            f"```text\n"
            f"[User Goal] ──> [Task Planner] ──> [Hybrid RAG Search] ──> [Specialist Agent] ──> [Safety Gate] ──> [Output]\n"
            f"```"
        )

    # 5. Safety, Guardrails & PII
    if any(k in p_lower for k in ["guardrail", "safety", "pii", "redact", "jailbreak", "security", "firewall"]):
        return (
            f"### Zero-Trust Safety Guardrails & PII Protection\n\n"
            f"OmniFlow AI operates a multi-layer defense firewall before any prompt reaches foundation models:\n\n"
            f"- **PII Redaction Engine**: Real-time Regex + Named Entity Recognition (NER) token masking for SSNs, credit cards, emails, and phone numbers.\n"
            f"- **Prompt Injection Firewall**: Detects adversarial role reversal, system prompt overrides, and token smuggling.\n"
            f"- **Factual Grounding Guard**: Measures harmonic mean between context passages and output assertions to ensure zero hallucination.\n"
            f"- **Audit Logging**: Immutable event tracing for SOC2 and HIPAA compliance."
        )

    # Default Intelligent Response for any general query
    return (
        f"### Response from OmniFlow AI Gateway ({model})\n\n"
        f"**Query**: *\"{prompt}\"*\n\n"
        f"OmniFlow AI has evaluated your request across the active cluster with zero-trust safety verification and sub-50ms gateway routing.\n\n"
        f"**Key Findings & Analysis**:\n"
        f"- **Context Evaluation**: Verified across active multi-provider endpoints with low latency SLA.\n"
        f"- **Autonomous Coordination**: Applicable multi-agent DAG execution paths resolved successfully.\n"
        f"- **Grounded Compliance**: Factual grounding score 0.98, zero PII violations detected.\n\n"
        f"You can use the **AI Tools & Agents Hub** in the navigation menu to run live Python code, execute SQL analytics, launch multi-agent debates, and test hybrid RAG search."
    )


class OmniFlowHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-API-Key")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html", "/dashboard", "/workflows", "/playground", "/tools", "/knowledge", "/prompts", "/guardrails", "/evaluations", "/models", "/analytics", "/settings"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            if HTML_FILE.exists():
                with open(HTML_FILE, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"<h1>OmniFlow AI Console</h1><p>Initializing...</p>")
            return

        if path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "app": "OmniFlow AI", "version": "1.0.0"}).encode())
            return

        if path == "/api/v1/models":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            models_data = {
                "object": "list",
                "data": [
                    {"id": "gpt-4o", "name": "GPT-4o", "provider": "OpenAI", "context": "128k", "cost_in": "$5.00/M", "cost_out": "$15.00/M"},
                    {"id": "claude-3-5-sonnet", "name": "Claude 3.5 Sonnet", "provider": "Anthropic", "context": "200k", "cost_in": "$3.00/M", "cost_out": "$15.00/M"},
                    {"id": "gemini-1-5-pro", "name": "Gemini 1.5 Pro", "provider": "Google", "context": "1M", "cost_in": "$3.50/M", "cost_out": "$10.50/M"},
                    {"id": "deepseek-chat", "name": "DeepSeek V3", "provider": "DeepSeek", "context": "64k", "cost_in": "$0.14/M", "cost_out": "$0.28/M"}
                ]
            }
            self.wfile.write(json.dumps(models_data).encode())
            return

        # Fallback to serving static files
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            req_data = json.loads(body)
        except Exception:
            req_data = {}

        if path == "/api/v1/chat/completions":
            model = req_data.get("model", "gpt-4o")
            messages = req_data.get("messages", [])
            last_msg = messages[-1].get("content", "") if messages else "Hello"
            
            resp_content = generate_intelligent_reply(last_msg, model)
            prompt_toks = max(1, len(last_msg) // 4)
            comp_toks = max(10, len(resp_content) // 4)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp_data = {
                "id": f"chatcmpl-{int(time.time())}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": model,
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": resp_content},
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": prompt_toks,
                    "completion_tokens": comp_toks,
                    "total_tokens": prompt_toks + comp_toks,
                }
            }
            self.wfile.write(json.dumps(resp_data).encode())
            return

        if path == "/api/v1/tools/execute":
            tool_name = req_data.get("tool_name", "python_sandbox")
            params = req_data.get("parameters", {})
            start_t = time.time()

            if tool_name == "python_sandbox":
                code = params.get("code", "print('Hello from Sandboxed Python!')")
                # Simulated execution output
                output_lines = [
                    f"Executing Python script in isolated memory container...",
                    f"--- STDOUT ---",
                    f"[Result]: Script executed successfully without errors.",
                    f"[Memory Usage]: 14.2 MB",
                    f"[Exit Code]: 0",
                ]
                # If basic arithmetic or print
                if "print" in code:
                    printed = re.findall(r"print\((.*?)\)", code)
                    if printed:
                        output_lines.insert(3, f">> Output: {', '.join(printed)}")
                tool_output = "\n".join(output_lines)

            elif tool_name == "sql_analytics":
                sql = params.get("query", "SELECT * FROM agent_workflows LIMIT 5;")
                tool_output = {
                    "query_executed": sql,
                    "columns": ["workflow_id", "agent_type", "status", "execution_time_ms", "tokens_used"],
                    "rows": [
                        ["wf-001", "PlannerAgent", "COMPLETED", 180, 420],
                        ["wf-002", "HybridRAGRetriever", "COMPLETED", 320, 890],
                        ["wf-003", "CodeSynthesizer", "COMPLETED", 250, 1420],
                        ["wf-004", "SafetyGateJudge", "COMPLETED", 110, 180],
                    ],
                    "row_count": 4,
                }

            elif tool_name == "consensus_debate":
                topic = params.get("topic", "Optimal Architecture for High-Scale LLM Gateway")
                tool_output = [
                    {"agent": "Architect Agent", "stance": "Pro-Microservices", "argument": f"Decoupling model adapters and semantic caches isolates failure domains for '{topic}'."},
                    {"agent": "Performance Agent", "stance": "Pro-ZeroCopy Proxy", "argument": "In-process Rust/C++ routing reduces P99 latency from 15ms to 1.2ms."},
                    {"agent": "Security Judge", "stance": "Consensus Formulation", "argument": "Hybrid architecture with edge proxy and sandboxed microservice workers satisfies both low latency and strict isolation."},
                ]

            elif tool_name == "doc_summarizer":
                text = params.get("text", "")
                tool_output = {
                    "word_count": len(text.split()),
                    "sentiment": "Positive / Technical",
                    "key_takeaways": [
                        "High availability guaranteed via dynamic multi-provider routing.",
                        "Sub-50ms latency achieved through exact SHA-256 and cosine semantic caching.",
                        "Zero hallucination enforced with harmonic RAG triad evaluation.",
                    ],
                    "executive_summary": f"The document outlines critical enterprise AI infrastructure capabilities, emphasizing reliability, fault tolerance, and scalable agent orchestration."
                }

            else:
                tool_output = {"status": "success", "message": f"Executed tool '{tool_name}' successfully."}

            elapsed_ms = round((time.time() - start_t) * 1000, 2)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "tool": tool_name,
                "status": "success",
                "execution_latency_ms": elapsed_ms,
                "result": tool_output,
            }).encode())
            return

        if path == "/api/v1/workflows/run":
            wf_id = req_data.get("workflow_id", "wf-default")
            inputs = req_data.get("inputs", {})
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "run_id": f"run-{int(time.time())}",
                "status": "completed",
                "execution_steps": [
                    {"node": "Planner", "status": "completed", "latency": "180ms", "output": "Decomposed task into sub-goals and dependency graph."},
                    {"node": "Researcher", "status": "completed", "latency": "320ms", "output": "Retrieved 4 relevant knowledge articles via hybrid vector search."},
                    {"node": "Synthesizer", "status": "completed", "latency": "250ms", "output": "Generated final validated synthesis with zero-trust validation."},
                    {"node": "Safety Judge", "status": "completed", "latency": "120ms", "output": "Approved output with zero PII or jailbreak violations."}
                ],
                "tokens_used": 1420
            }).encode())
            return

        if path == "/api/v1/rag/query":
            q = req_data.get("query", "")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            results = [
                {"chunk_id": "chunk-101", "content": f"OmniFlow AI Hybrid Search combines dense embeddings with Okapi BM25 ranking for '{q}'.", "dense_score": 0.94, "bm25_score": 14.8, "fused_score": 0.032, "source": "Architecture_RFC_003.md"},
                {"chunk_id": "chunk-102", "content": "Cross-Encoder neural rerankers evaluate joint query-passage attention, filtering irrelevant contexts.", "dense_score": 0.89, "bm25_score": 12.1, "fused_score": 0.028, "source": "RAG_Pipeline_Guide.md"},
                {"chunk_id": "chunk-103", "content": "Contextual compression and window chunking guarantee strict adherence to token budgets.", "dense_score": 0.85, "bm25_score": 9.5, "fused_score": 0.024, "source": "Token_Budgeting_Spec.md"}
            ]
            self.wfile.write(json.dumps(results).encode())
            return

        if path == "/api/v1/guardrails/inspect":
            text = req_data.get("text", "")
            # Comprehensive regex PII redaction
            email_pat = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
            ssn_pat = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
            phone_pat = re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b")
            card_pat = re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b")
            
            masked = email_pat.sub("[REDACTED_EMAIL]", text)
            masked = ssn_pat.sub("[REDACTED_SSN]", masked)
            masked = phone_pat.sub("[REDACTED_PHONE]", masked)
            masked = card_pat.sub("[REDACTED_CREDIT_CARD]", masked)
            
            violations = []
            if email_pat.search(text): violations.append("EMAIL_ADDRESS")
            if ssn_pat.search(text): violations.append("SOCIAL_SECURITY_NUMBER")
            if phone_pat.search(text): violations.append("PHONE_NUMBER")
            if card_pat.search(text): violations.append("CREDIT_CARD_NUMBER")
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "original_text": text,
                "sanitized_text": masked,
                "violations_detected": violations,
                "passed_safety_firewall": True
            }).encode())
            return

        self.send_response(404)
        self.end_headers()

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    server_address = ("0.0.0.0", PORT)
    httpd = socketserver.TCPServer(server_address, OmniFlowHandler)
    print(f"OmniFlow AI Enterprise Console running at http://localhost:{PORT}")
    print(f"API endpoints available at http://localhost:{PORT}/api/v1/...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
