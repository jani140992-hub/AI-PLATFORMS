"""OmniFlow AI Enterprise API Application Entrypoint."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import time

from app.core.config import settings
from app.api.v1.endpoints import chat, agents, workflows, rag, prompts, evaluations, models
from app.api.v1.websockets import streaming
from app.telemetry.metrics import metrics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown hooks."""
    print(f"Starting {settings.APP_NAME} in {settings.APP_ENV} mode...")
    yield
    print(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise Multi-Agent & LLMOps Platform API Gateway",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Track request count and latency for Prometheus."""
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    metrics.record_http_request(request.method, request.url.path, response.status_code)
    return response


# Include Routers
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=["Chat & Completions"])
app.include_router(agents.router, prefix=settings.API_V1_STR, tags=["Agents"])
app.include_router(workflows.router, prefix=settings.API_V1_STR, tags=["Workflows"])
app.include_router(rag.router, prefix=settings.API_V1_STR, tags=["RAG & Knowledge"])
app.include_router(prompts.router, prefix=settings.API_V1_STR, tags=["Prompt Registry"])
app.include_router(evaluations.router, prefix=settings.API_V1_STR, tags=["Evaluations"])
app.include_router(models.router, prefix=settings.API_V1_STR, tags=["Model Catalog"])
app.include_router(streaming.router, prefix="/api/v1", tags=["WebSockets"])


@app.get("/health", tags=["System"])
async def health_check():
    """System health check endpoint."""
    return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/metrics", response_class=PlainTextResponse, tags=["Observability"])
async def prometheus_metrics():
    """Prometheus metrics scrape endpoint."""
    return metrics.generate_prometheus_export()
