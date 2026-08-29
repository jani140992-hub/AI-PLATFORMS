"""Comprehensive Enterprise Error Hierarchy.

Defines standardized exception classes across the gateway, agents, RAG, and governance engines.
"""

from typing import Any, Dict, Optional


class OmniFlowException(Exception):
    """Base exception for all domain errors within OmniFlow AI."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class EntityNotFoundError(OmniFlowException):
    """Raised when a requested resource or entity does not exist."""

    def __init__(self, entity_name: str, entity_id: Any):
        super().__init__(
            message=f"{entity_name} with identifier '{entity_id}' not found.",
            code="ENTITY_NOT_FOUND",
            details={"entity_name": entity_name, "entity_id": str(entity_id)},
        )


class AuthenticationError(OmniFlowException):
    """Raised when authentication credentials are missing, invalid, or expired."""

    def __init__(self, message: str = "Invalid or expired authentication credentials."):
        super().__init__(message=message, code="AUTHENTICATION_FAILED")


class AuthorizationError(OmniFlowException):
    """Raised when the user or tenant lacks required permissions for the action."""

    def __init__(self, message: str = "Insufficient permissions to perform this operation."):
        super().__init__(message=message, code="PERMISSION_DENIED")


class RateLimitExceededError(OmniFlowException):
    """Raised when an API key, tenant, or user exceeds rate limit thresholds."""

    def __init__(self, retry_after: int, message: str = "Rate limit threshold exceeded."):
        super().__init__(
            message=message,
            code="RATE_LIMIT_EXCEEDED",
            details={"retry_after_seconds": retry_after},
        )


class TokenBudgetExceededError(OmniFlowException):
    """Raised when a tenant or workspace exceeds monthly token quota."""

    def __init__(self, current_usage: int, limit: int):
        super().__init__(
            message=f"Monthly token budget exceeded: {current_usage}/{limit} tokens used.",
            code="TOKEN_BUDGET_EXCEEDED",
            details={"current_usage": current_usage, "limit": limit},
        )


class ModelProviderError(OmniFlowException):
    """Raised when an external model provider (OpenAI, Anthropic, etc.) fails."""

    def __init__(self, provider: str, status_code: int, raw_error: str):
        super().__init__(
            message=f"Upstream model provider '{provider}' returned error: {raw_error}",
            code="PROVIDER_ERROR",
            details={"provider": provider, "status_code": status_code, "raw_error": raw_error},
        )


class WorkflowExecutionError(OmniFlowException):
    """Raised when an agent workflow graph execution encounters an unrecoverable failure."""

    def __init__(self, workflow_id: str, node_id: str, message: str):
        super().__init__(
            message=f"Workflow '{workflow_id}' failed at node '{node_id}': {message}",
            code="WORKFLOW_EXECUTION_FAILED",
            details={"workflow_id": workflow_id, "node_id": node_id},
        )


class InvalidWorkflowGraphError(OmniFlowException):
    """Raised when a workflow DAG contains invalid edges, disconnected components, or illegal cycles."""

    def __init__(self, message: str, violations: list[str]):
        super().__init__(
            message=message,
            code="INVALID_WORKFLOW_GRAPH",
            details={"violations": violations},
        )


class SafetyViolationError(OmniFlowException):
    """Raised when a prompt or completion violates configured safety guardrails."""

    def __init__(self, rule_name: str, rule_type: str, violation_details: str):
        super().__init__(
            message=f"Safety guardrail '{rule_name}' triggered: {violation_details}",
            code="SAFETY_GUARDRAIL_VIOLATION",
            details={"rule_name": rule_name, "rule_type": rule_type, "violation": violation_details},
        )


class RAGIngestionError(OmniFlowException):
    """Raised when document extraction, parsing, or vector indexing fails."""

    def __init__(self, document_id: str, stage: str, message: str):
        super().__init__(
            message=f"RAG ingestion failed for document '{document_id}' during stage '{stage}': {message}",
            code="RAG_INGESTION_FAILED",
            details={"document_id": document_id, "stage": stage},
        )
