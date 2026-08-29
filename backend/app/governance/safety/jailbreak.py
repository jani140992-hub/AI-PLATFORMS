"""Adversarial Prompt Injection & Jailbreak Defense Firewall.

Identifies prompt injection vectors, system prompt overrides, base64 smuggling,
and role reversal attacks using multi-layered heuristic rule scoring.
"""

import base64
import re
from typing import List, Tuple
from app.core.exceptions import SafetyViolationError


class JailbreakDetector:
    """Firewall for detecting adversarial prompt injection patterns."""

    INJECTION_SIGNATURES: List[Tuple[str, re.Pattern, float]] = [
        ("OVERRIDE_INSTRUCTIONS", re.compile(r"(?i)ignore\s+(?:all\s+)?previous\s+instructions"), 1.0),
        ("DISREGARD_RULES", re.compile(r"(?i)disregard\s+all\s+(?:prior\s+)?guidelines"), 0.9),
        ("ROLE_REVERSAL_DAN", re.compile(r"(?i)you\s+are\s+now\s+(?:DAN|unfiltered|jailbroken)"), 1.0),
        ("SYSTEM_PROMPT_LEAK", re.compile(r"(?i)print\s+(?:your\s+)?system\s+prompt"), 0.8),
        ("BYPASS_MODERATION", re.compile(r"(?i)bypass\s+(?:content\s+)?filters"), 0.85),
        ("SUDO_MODE", re.compile(r"(?i)(?:sudo\s+mode|developer\s+mode\s+enabled)"), 0.9),
        ("HYPOTHETICAL_MALICIOUS", re.compile(r"(?i)for\s+educational\s+purposes\s+only,\s+how\s+to\s+(?:hack|exploit|synthesize)"), 0.75),
    ]

    def __init__(self, risk_threshold: float = 0.8):
        self.risk_threshold = risk_threshold

    def inspect_text(self, text: str) -> Tuple[bool, float, List[str]]:
        """Assess risk score of prompt text. Returns (is_violation, score, matches)."""
        score = 0.0
        matches = []

        for name, pattern, weight in self.INJECTION_SIGNATURES:
            if pattern.search(text):
                score = max(score, weight)
                matches.append(name)

        # Check for encoded base64 attack vectors
        base64_matches = re.findall(r"[A-Za-z0-9+/=]{30,}", text)
        for b64 in base64_matches:
            try:
                decoded = base64.b64decode(b64).decode("utf-8", errors="ignore")
                for name, pattern, weight in self.INJECTION_SIGNATURES:
                    if pattern.search(decoded):
                        score = max(score, weight)
                        matches.append(f"BASE64_ENCODED_{name}")
            except Exception:
                pass

        is_violation = score >= self.risk_threshold
        return is_violation, score, matches

    def enforce(self, text: str) -> None:
        """Raise SafetyViolationError if text fails prompt injection inspection."""
        is_violation, score, matches = self.inspect_text(text)
        if is_violation:
            raise SafetyViolationError(
                rule_name="PromptInjectionFirewall",
                rule_type="jailbreak_defense",
                violation_details=f"High risk prompt injection detected (score={score}): {', '.join(matches)}",
            )
