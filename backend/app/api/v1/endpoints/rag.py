"""RAG Knowledge Base & Document Ingestion Endpoints."""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel
import uuid

from app.api.deps import AuthContext, get_auth_context
from app.rag.pipeline import RAGPipeline

router = APIRouter()
rag_pipeline = RAGPipeline()


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/rag/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    knowledge_base_id: str = Form("default_kb"),
    auth: AuthContext = Depends(get_auth_context),
) -> Dict[str, Any]:
    """Upload and ingest a document into the Knowledge Base."""
    content = await file.read()
    doc_id = str(uuid.uuid4())
    chunks_indexed = await rag_pipeline.ingest_document(content, file.filename or "doc.txt", doc_id)
    return {
        "document_id": doc_id,
        "filename": file.filename,
        "chunks_indexed": chunks_indexed,
        "status": "indexed",
    }


@router.post("/rag/query")
async def query_knowledge_base(
    req: QueryRequest,
    auth: AuthContext = Depends(get_auth_context),
) -> List[Dict[str, Any]]:
    """Perform hybrid search and reranking on knowledge base."""
    results = await rag_pipeline.query(req.query, top_k=req.top_k)
    return [r.model_dump() for r in results]
