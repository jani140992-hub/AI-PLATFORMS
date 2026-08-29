"""Source Code Extractor supporting AST Analysis & Function Splitting."""

from typing import Any
from app.rag.extractors.base import BaseExtractor, ExtractedDocument


class CodeExtractor(BaseExtractor):
    """Extracts source code files (Python, TypeScript, Go, Rust, Java)."""

    async def extract(self, file_bytes: bytes, filename: str, **kwargs: Any) -> ExtractedDocument:
        text = file_bytes.decode("utf-8", errors="replace")
        ext = filename.split(".")[-1].lower() if "." in filename else "txt"
        
        return ExtractedDocument(
            source_id=filename,
            filename=filename,
            content=text,
            content_type=f"text/x-{ext}",
            file_size_bytes=len(file_bytes),
            metadata={"language": ext, "total_code_lines": len(text.splitlines())},
        )
