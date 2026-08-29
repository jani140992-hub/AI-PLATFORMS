"""Regex & Pattern-Based PII (Personally Identifiable Information) Redaction Engine.

Detects and masks Social Security Numbers, Credit Card Numbers, Email Addresses,
Phone Numbers, IP Addresses, API Keys, and JWT Tokens.
"""

import re
from typing import Dict, List, Tuple


class PIIRedactor:
    """Enterprise PII detection and token substitution filter."""

    PATTERNS: Dict[str, re.Pattern] = {
        "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
        "PHONE_US": re.compile(r"\b(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})\b"),
        "SSN": re.compile(r"\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b"),
        "CREDIT_CARD": re.compile(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"),
        "IPV4": re.compile(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"),
        "API_KEY": re.compile(r"\b(?:sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}|omniflow_[a-zA-Z0-9]{20,})\b"),
        "JWT": re.compile(r"\beyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\b"),
    }

    def __init__(self, mask_format: str = "[REDACTED_{type}]"):
        self.mask_format = mask_format

    def redact(self, text: str) -> Tuple[str, List[Dict[str, str]]]:
        """Scrub PII from text and return masked text along with audit violation entries."""
        sanitized = text
        redacted_entries: List[Dict[str, str]] = []

        for pii_type, pattern in self.PATTERNS.items():
            matches = list(pattern.finditer(sanitized))
            for match in reversed(matches):
                original_value = match.group(0)
                mask = self.mask_format.format(type=pii_type)
                sanitized = sanitized[:match.start()] + mask + sanitized[match.end():]
                redacted_entries.append({
                    "type": pii_type,
                    "masked_placeholder": mask,
                    "char_span": f"{match.start()}:{match.end()}",
                })

        return sanitized, redacted_entries
