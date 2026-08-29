import http.server
import json
import socketserver
import sys
import threading
import time
import urllib.parse
from pathlib import Path

PORT = 3000
HTML_FILE = Path(__file__).parent / "static" / "index.html"

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

        if path in ("/", "/index.html", "/dashboard", "/workflows", "/playground", "/knowledge", "/prompts", "/guardrails", "/evaluations", "/models", "/analytics", "/settings"):
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
            
            # Formulate simulated intelligent response based on prompt
            resp_content = f"[OmniFlow Gateway - {model}]: Processed request successfully.\\n\\nResponse to \\\"{last_msg}\\\":\\n\\nOmniFlow AI orchestrates multi-agent workflows with state graphs, hybrid vector search (Dense + BM25), and zero-trust safety guardrails. Execution verified across active providers with 99.98% reliability."
            
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
                "usage": {"prompt_tokens": len(last_msg)//4 + 5, "completion_tokens": 68, "total_tokens": len(last_msg)//4 + 73}
            }
            self.wfile.write(json.dumps(resp_data).encode())
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
                    {"node": "Planner", "status": "completed", "latency": "180ms", "output": "Decomposed task into sub-goals."},
                    {"node": "Researcher", "status": "completed", "latency": "320ms", "output": "Retrieved 4 relevant knowledge articles via hybrid search."},
                    {"node": "Synthesizer", "status": "completed", "latency": "250ms", "output": "Generated final validated synthesis."}
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
            # Simple PII simulation
            import re
            email_pat = re.compile(r"\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b")
            ssn_pat = re.compile(r"\\b\\d{3}-\\d{2}-\\d{4}\\b")
            masked = email_pat.sub("[REDACTED_EMAIL]", text)
            masked = ssn_pat.sub("[REDACTED_SSN]", masked)
            violations = []
            if email_pat.search(text): violations.append("EMAIL_ADDRESS")
            if ssn_pat.search(text): violations.append("SOCIAL_SECURITY_NUMBER")
            
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
    server_address = ("0.0.0.0", PORT)
    httpd = socketserver.TCPServer(server_address, OmniFlowHandler)
    print(f"OmniFlow AI Enterprise Console running at http://localhost:{PORT}")
    print(f"API endpoints available at http://localhost:{PORT}/api/v1/...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
