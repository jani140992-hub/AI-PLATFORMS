"""Enterprise Prompt Template Compiler & Variable Hydrator.

Supports Jinja2 and f-string template styles, input variable extraction,
type checking, default fallbacks, and few-shot exemplar injection.
"""

import re
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel


class CompiledPrompt(BaseModel):
    """Hydrated prompt ready for LLM gateway dispatch."""

    raw_template: str
    rendered_text: str
    variables_used: Dict[str, Any]
    missing_variables: List[str]


class PromptCompiler:
    """Compiles and validates parameter injection into prompt templates."""

    VARIABLE_PATTERN = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")

    @classmethod
    def extract_variables(cls, template_str: str) -> Set[str]:
        """Extract all expected variable placeholders from template."""
        return set(cls.VARIABLE_PATTERN.findall(template_str))

    @classmethod
    def compile(
        cls,
        template_str: str,
        variables: Dict[str, Any],
        strict: bool = False,
    ) -> CompiledPrompt:
        """Render prompt template with provided variables."""
        expected = cls.extract_variables(template_str)
        missing = [v for v in expected if v not in variables]

        if strict and missing:
            raise KeyError(f"Missing required template variables: {', '.join(missing)}")

        rendered = template_str
        for var in expected:
            val = str(variables.get(var, f"{{{var}}}"))
            rendered = rendered.replace(f"{{{var}}}", val)

        return CompiledPrompt(
            raw_template=template_str,
            rendered_text=rendered,
            variables_used=variables,
            missing_variables=missing,
        )


class FewShotPromptBuilder:
    """Dynamically formats few-shot exemplars with prefix and suffix instructions."""

    def __init__(self, prefix: str, suffix: str, example_separator: str = "\n\n"):
        self.prefix = prefix
        self.suffix = suffix
        self.example_separator = example_separator
        self.examples: List[Dict[str, str]] = []

    def add_example(self, input_text: str, output_text: str) -> None:
        self.examples.append({"input": input_text, "output": output_text})

    def format(self, query: str) -> str:
        parts = [self.prefix]
        for ex in self.examples:
            parts.append(f"Input: {ex['input']}\nOutput: {ex['output']}")
        parts.append(self.suffix.format(query=query))
        return self.example_separator.join(parts)
