# OmniFlow AI - Enterprise Multi-Agent & LLMOps Platform

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![TypeScript](https://img.shields.io/badge/typescript-5.4+-blue.svg)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/docker-ready-green.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-helm-326ce5.svg)](https://helm.sh/)

**OmniFlow AI** is a production-grade, cloud-native Enterprise AI Platform engineered for orchestrating autonomous multi-agent systems, intelligent LLM gateway routing, hybrid RAG knowledge pipelines, model evaluation harnesses, prompt lifecycle management, and real-time observability.

---

## Key Platform Capabilities

### 1. Multi-Provider AI Gateway & Intelligent Router
- Unified OpenAI-compatible API interface supporting OpenAI, Anthropic Claude, Google Gemini, DeepSeek, AWS Bedrock, Azure OpenAI, Mistral, Ollama, and vLLM.
- Dynamic cost- and latency-optimized routing with automatic circuit-breaking and fallback cascades.
- Distributed semantic caching powered by vector embeddings and Redis Cosine similarity matching.
- Token rate limiting, user quota budgeting, and enterprise tenant billing attribution.

### 2. Graph-Based Multi-Agent Orchestration
- State-machine driven Directed Acyclic Graph (DAG) and cyclic graph execution engine.
- Parallel fan-out/fan-in node dispatching with human-in-the-loop approval gates.
- Multi-tier memory architecture: Working Memory, Semantic Vector Memory, and Episodic Reflection Buffers.
- Secure, sandboxed tool execution engine with built-in connectors for Python REPL, SQL engines, web search, and vector search.
- Multi-agent collaboration paradigms: Hierarchical Coordinator, Consensus Voting, and Peer-to-Peer delegation.

### 3. Enterprise Hybrid RAG & Knowledge Hub
- Multimodal document ingestion supporting PDF, DOCX, Markdown, HTML, CSV, JSON, and source code.
- Advanced chunking strategies: Recursive Character, Semantic Boundary, Markdown Hierarchy, and Token Window.
- Hybrid search fusing Dense Vector Embeddings with Sparse Lexical BM25 via Reciprocal Rank Fusion (RRF).
- Cross-Encoder neural reranking pipeline for maximum precision.
- Vector database connectors for PostgreSQL pgvector, Qdrant, Pinecone, Milvus, ChromaDB, and Weaviate.

### 4. Safety Guardrails & Model Governance
- Real-time PII detection and redaction using hybrid Regex and Named Entity Recognition (NER).
- Adversarial jailbreak and prompt injection firewalls.
- Toxic content, bias, and profanity classification filters.
- Output hallucination detection and JSON schema enforcement.

### 5. Evaluation & LLM-as-a-Judge Harness
- Automated test harnesses for standard benchmarks: MMLU, GSM8K, HumanEval, ARC, and TruthfulQA.
- RAG Triad evaluation: Context Relevance, Groundedness (Faithfulness), and Answer Relevance.
- Synthetic Q&A dataset generation from indexed enterprise documents.
- Continuous model benchmarking with automated cost and latency profiling.

### 6. Developer SDKs & Visual Web Console
- Official Python Client SDK (`omniflow-py`) with async/sync support and agent decorators.
- Official TypeScript Client SDK (`@omniflow/sdk`) with SSE streaming parsers.
- Next.js 14 / React modern web console featuring a visual drag-and-drop workflow canvas, streaming chat playground, prompt studio, and observability dashboards.

---

## Repository Architecture

```
AI-PLATFORMS/
├── backend/                  # FastAPI Enterprise Backend Services
│   ├── app/
│   │   ├── api/              # RESTful & Streaming WebSocket Endpoints
│   │   ├── core/             # Configuration, Security, DB Engine, Events
│   │   ├── db/               # SQLAlchemy Models, Repositories, Migrations
│   │   ├── gateway/          # Multi-LLM Routing, Cache, Providers
│   │   ├── agents/           # Multi-Agent Graph Engine & Memory
│   │   ├── rag/              # Ingestion, Hybrid Search & Reranking
│   │   ├── governance/       # Guardrails, Safety, Prompt Registry
│   │   ├── services/         # Async Background Workers & Orchestration
│   │   └── telemetry/        # OpenTelemetry Traces, Prometheus Metrics
│   ├── alembic/              # Database Schema Migrations
│   └── tests/                # Comprehensive Pytest Test Suites
├── frontend/                 # Next.js 14 Enterprise Web Console
│   ├── src/
│   │   ├── app/              # Next.js App Router Pages
│   │   ├── components/       # Visual Workflow Builder, Chat, Analytics UI
│   │   ├── hooks/            # Custom React State Hooks
│   │   ├── lib/              # Client API, Utilities, Stores
│   │   └── types/            # TypeScript Interface Definitions
│   └── public/               # Static Web Assets
├── sdks/
│   ├── python/               # Official Python SDK (omniflow-py)
│   └── typescript/           # Official TypeScript SDK (@omniflow/sdk)
├── deployments/              # Production Infrastructure
│   ├── docker/               # Multi-stage Dockerfiles & Docker Compose
│   ├── helm/                 # Production Kubernetes Helm Charts
│   └── terraform/            # Multi-Cloud IaC (AWS / GCP)
├── docs/                     # RFCs, Specifications & Guides
└── scripts/                  # Seed Scripts, Benchmarks & Utilities
```

---

## Getting Started

### Quickstart with Docker Compose

```bash
# Clone the repository
git clone git@github.com:jani140992-hub/AI-PLATFORMS.git
cd AI-PLATFORMS

# Copy environment variables
cp .env.example .env

# Launch all services (Postgres, Redis, Qdrant, Backend, Worker, Frontend)
docker-compose -f deployments/docker/docker-compose.yml up -d
```

Access the web console at `http://localhost:3000` and the API documentation at `http://localhost:8000/docs`.

### Local Development Setup

```bash
# Backend setup
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# Frontend setup
cd ../frontend
npm install
npm run dev
```

---

## License

OmniFlow AI is open-source software licensed under the [Apache 2.0 License](LICENSE).
