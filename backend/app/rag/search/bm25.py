"""Full BM25 (Best Matching 25) Lexical Retrieval Engine.

Implements Okapi BM25 scoring with term frequency saturation (k1),
document length normalization (b), and inverse document frequency (IDF) weighting.
"""

import math
import re
from typing import Dict, List, Set, Tuple


class BM25Index:
    """In-memory Okapi BM25 index with tokenization and inverted index."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.doc_ids: List[str] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_length: float = 0.0
        self.corpus_size: int = 0
        self.doc_freqs: Dict[str, int] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = {}  # term -> {doc_idx: freq}
        self.stopwords: Set[str] = {
            "a", "an", "the", "in", "on", "at", "and", "or", "of", "to", "is", "it", "for", "with"
        }

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r"\b[a-zA-Z0-9_-]+\b", text.lower())
        return [w for w in words if w not in self.stopwords and len(w) > 1]

    def add_documents(self, doc_ids: List[str], documents: List[str]) -> None:
        """Tokenize and index a collection of documents."""
        start_idx = len(self.doc_ids)
        for i, (doc_id, doc_text) in enumerate(zip(doc_ids, documents)):
            current_idx = start_idx + i
            self.doc_ids.append(doc_id)
            tokens = self._tokenize(doc_text)
            self.doc_lengths.append(len(tokens))

            # Count frequencies
            frequencies: Dict[str, int] = {}
            for t in tokens:
                frequencies[t] = frequencies.get(t, 0) + 1

            for t, freq in frequencies.items():
                if t not in self.inverted_index:
                    self.inverted_index[t] = {}
                self.inverted_index[t][current_idx] = freq
                self.doc_freqs[t] = self.doc_freqs.get(t, 0) + 1

        self.corpus_size = len(self.doc_ids)
        self.avg_doc_length = sum(self.doc_lengths) / float(self.corpus_size) if self.corpus_size > 0 else 0.0

    def search(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Compute BM25 scores for all matching documents."""
        query_tokens = self._tokenize(query)
        if not query_tokens or self.corpus_size == 0:
            return []

        scores: Dict[int, float] = {}

        for term in query_tokens:
            if term not in self.inverted_index:
                continue

            df = self.doc_freqs[term]
            # IDF formula: log((N - df + 0.5) / (df + 0.5) + 1)
            idf = math.log((self.corpus_size - df + 0.5) / (df + 0.5) + 1.0)

            for doc_idx, freq in self.inverted_index[term].items():
                doc_len = self.doc_lengths[doc_idx]
                numerator = freq * (self.k1 + 1.0)
                denominator = freq + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_length))
                term_score = idf * (numerator / denominator)
                scores[doc_idx] = scores.get(doc_idx, 0.0) + term_score

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [(self.doc_ids[idx], score) for idx, score in ranked]
