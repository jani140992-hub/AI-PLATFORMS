"""Markdown and Plaintext Extractor with Header Hierarchy Preservation."""

from typing import Any
from app.rag.extractors.base import BaseExtractor, ExtractedDocument


class MarkdownExtractor(BaseExtractor):
    """Extracts Markdown content, preserving hierarchical section anchors."""

    async def extract(self, file_bytes: bytes, filename: str, **kwargs: Any) -> ExtractedDocument:
        text = file_bytes.decode("utf-8", errors="replace")
        
        # Analyze heading tags
        headings = []
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                headings.append(stripped)

        return ExtractedDocument(
            source_id=filename,
            filename=filename,
            content=text,
            content_type="text/markdown",
            file_size_bytes=len(file_bytes),
            metadata={"headings": headings, "heading_count": len(headings)},
        )
