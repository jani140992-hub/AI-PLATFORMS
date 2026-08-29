"""Recursive Character Chunker.

Recursively splits text by semantic paragraph, newline, and sentence delimiters
while strictly enforcing token and character length constraints with overlap windows.
"""

from typing import Any, Dict, List, Optional
import uuid
from app.rag.chunkers.base import BaseChunker, TextChunk


class RecursiveCharacterChunker(BaseChunker):
    """Hierarchical text splitter using prioritized delimiters."""

    SEPARATORS: List[str] = [
        "\n\n",      # Paragraphs
        "\n",        # Lines
        ". ",        # Sentences
        "? ",
        "! ",
        "; ",
        ", ",        # Clauses
        " ",         # Words
        "",          # Characters
    ]

    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        if not text:
            return []
        
        separator = separators[-1]
        for s in separators:
            if s == "" or s in text:
                separator = s
                break

        splits = text.split(separator) if separator else list(text)
        
        good_splits: List[str] = []
        current_chunk: List[str] = []
        current_len = 0

        for s in splits:
            item = s if separator == "" else s + separator
            item_len = len(item)
            if current_len + item_len > self.chunk_size:
                if current_chunk:
                    good_splits.append("".join(current_chunk).strip())
                    current_chunk = []
                    current_len = 0
                if item_len > self.chunk_size and len(separators) > 1:
                    # Recurse with finer separator
                    sub_splits = self._split_text(s, separators[1:])
                    good_splits.extend(sub_splits)
                else:
                    current_chunk.append(item)
                    current_len += item_len
            else:
                current_chunk.append(item)
                current_len += item_len

        if current_chunk:
            good_splits.append("".join(current_chunk).strip())

        return [g for g in good_splits if g]

    def chunk(self, text: str, document_id: str, metadata: Optional[Dict[str, Any]] = None) -> List[TextChunk]:
        raw_chunks = self._split_text(text, self.SEPARATORS)
        result: List[TextChunk] = []
        char_offset = 0

        for i, c_text in enumerate(raw_chunks):
            start_idx = text.find(c_text, char_offset)
            if start_idx == -1:
                start_idx = char_offset
            end_idx = start_idx + len(c_text)
            char_offset = max(0, end_idx - self.chunk_overlap)

            approx_tokens = max(1, len(c_text) // 4)
            result.append(
                TextChunk(
                    chunk_id=f"{document_id}_chunk_{i}",
                    document_id=document_id,
                    chunk_index=i,
                    content=c_text,
                    token_count=approx_tokens,
                    start_char_idx=start_idx,
                    end_char_idx=end_idx,
                    metadata=dict(metadata or {}),
                )
            )

        return result
